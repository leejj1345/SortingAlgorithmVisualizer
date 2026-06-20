from __future__ import annotations

from random import randint
from time import perf_counter

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


# 화면의 복잡도 비교표와 API 응답에서 함께 사용하는 알고리즘 메타데이터입니다.
ALGORITHM_INFO = {
    "bubble": {"name": "Bubble Sort", "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "selection": {"name": "Selection Sort", "best": "O(n²)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "insertion": {"name": "Insertion Sort", "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "merge": {"name": "Merge Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(n)"},
    "quick": {"name": "Quick Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)", "space": "O(log n)"},
    "heap": {"name": "Heap Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(1)"},
}


class SortRecorder:
    """정렬 과정의 배열 상태와 연산 횟수를 애니메이션 단계로 기록합니다."""

    def __init__(self, values: list[int], record_steps: bool = True):
        # 호출자가 전달한 원본 배열이 변경되지 않도록 복사본을 사용합니다.
        self.values = values[:]
        self.comparisons = 0
        self.swaps = 0
        self.steps: list[dict] = []
        self.record_steps = record_steps
        if record_steps:
            self.capture([], [], "준비")

    def capture(self, active: list[int], sorted_indices: list[int] | None = None, message: str = "") -> None:
        """현재 배열과 강조할 인덱스를 하나의 애니메이션 프레임으로 저장합니다."""
        if self.record_steps:
            self.steps.append({
                "values": self.values[:],
                "active": active,
                "sorted": sorted_indices or [],
                "comparisons": self.comparisons,
                "swaps": self.swaps,
                "message": message,
            })


def bubble_sort(r: SortRecorder) -> None:
    """인접 원소를 비교하여 큰 값을 배열 오른쪽부터 확정합니다."""
    n = len(r.values)
    for end in range(n - 1, 0, -1):
        # 한 회전에서 교환이 없으면 이미 정렬된 상태이므로 조기 종료합니다.
        changed = False
        for i in range(end):
            r.comparisons += 1
            r.capture([i, i + 1], list(range(end + 1, n)), "인접 원소 비교")
            if r.values[i] > r.values[i + 1]:
                r.values[i], r.values[i + 1] = r.values[i + 1], r.values[i]
                r.swaps += 1
                changed = True
                r.capture([i, i + 1], list(range(end + 1, n)), "교환")
        if not changed:
            break


def selection_sort(r: SortRecorder) -> None:
    """정렬되지 않은 구간의 최솟값을 찾아 앞쪽에 배치합니다."""
    n = len(r.values)
    for i in range(n - 1):
        minimum = i
        for j in range(i + 1, n):
            r.comparisons += 1
            r.capture([minimum, j], list(range(i)), "최솟값 탐색")
            if r.values[j] < r.values[minimum]:
                minimum = j
        if minimum != i:
            r.values[i], r.values[minimum] = r.values[minimum], r.values[i]
            r.swaps += 1
            r.capture([i, minimum], list(range(i)), "최솟값을 앞으로 이동")


def insertion_sort(r: SortRecorder) -> None:
    """현재 값을 왼쪽의 정렬된 구간에서 알맞은 위치에 삽입합니다."""
    for i in range(1, len(r.values)):
        # 이동 중 값이 덮어써지지 않도록 삽입할 값을 별도로 보관합니다.
        key = r.values[i]
        j = i - 1
        while j >= 0:
            r.comparisons += 1
            r.capture([j, j + 1], list(range(i)), "삽입 위치 비교")
            if r.values[j] <= key:
                break
            r.values[j + 1] = r.values[j]
            r.swaps += 1
            r.capture([j, j + 1], [], "오른쪽으로 이동")
            j -= 1
        r.values[j + 1] = key


def merge_sort(r: SortRecorder) -> None:
    """배열을 재귀적으로 분할한 뒤 정렬된 두 부분 배열을 병합합니다."""

    def merge(left: int, mid: int, right: int) -> None:
        # 원본 구간을 임시 배열 두 개로 복사한 뒤 작은 값부터 다시 기록합니다.
        a = r.values[left : mid + 1]
        b = r.values[mid + 1 : right + 1]
        i = j = 0
        k = left
        while i < len(a) and j < len(b):
            r.comparisons += 1
            r.capture([left + i, mid + 1 + j], [], "두 부분 배열 비교")
            if a[i] <= b[j]:
                r.values[k] = a[i]
                i += 1
            else:
                r.values[k] = b[j]
                j += 1
            # 병합 정렬은 직접 교환하지 않으므로 원본 배열에 쓴 횟수를 집계합니다.
            r.swaps += 1
            r.capture([k], [], "병합하여 쓰기")
            k += 1
        while i < len(a):
            r.values[k] = a[i]
            r.swaps += 1
            r.capture([k], [], "남은 원소 쓰기")
            i += 1
            k += 1
        while j < len(b):
            r.values[k] = b[j]
            r.swaps += 1
            r.capture([k], [], "남은 원소 쓰기")
            j += 1
            k += 1

    def divide(left: int, right: int) -> None:
        # 원소가 하나인 구간은 이미 정렬되어 있으므로 재귀를 종료합니다.
        if left >= right:
            return
        mid = (left + right) // 2
        divide(left, mid)
        divide(mid + 1, right)
        merge(left, mid, right)

    divide(0, len(r.values) - 1)


def quick_sort(r: SortRecorder) -> None:
    """마지막 원소를 피벗으로 사용하는 Lomuto 방식의 퀵 정렬입니다."""

    def partition(low: int, high: int) -> int:
        # i 앞쪽에는 피벗보다 작거나 같은 값만 유지합니다.
        pivot = r.values[high]
        i = low
        for j in range(low, high):
            r.comparisons += 1
            r.capture([j, high], [], f"피벗 {pivot}과 비교")
            if r.values[j] <= pivot:
                if i != j:
                    r.values[i], r.values[j] = r.values[j], r.values[i]
                    r.swaps += 1
                    r.capture([i, j], [], "피벗보다 작은 값 이동")
                i += 1
        # 피벗을 두 구간의 경계에 놓아 최종 위치를 확정합니다.
        if i != high:
            r.values[i], r.values[high] = r.values[high], r.values[i]
            r.swaps += 1
            r.capture([i, high], [], "피벗 위치 확정")
        return i

    def sort(low: int, high: int) -> None:
        if low < high:
            pivot = partition(low, high)
            sort(low, pivot - 1)
            sort(pivot + 1, high)

    sort(0, len(r.values) - 1)


def heap_sort(r: SortRecorder) -> None:
    """최대 힙을 구성하고 최댓값을 배열 뒤쪽부터 확정합니다."""

    def heapify(size: int, root: int) -> None:
        # 루트와 두 자식을 비교하여 가장 큰 값이 루트에 오도록 재구성합니다.
        largest = root
        left, right = root * 2 + 1, root * 2 + 2
        if left < size:
            r.comparisons += 1
            r.capture([largest, left], list(range(size, len(r.values))), "왼쪽 자식 비교")
            if r.values[left] > r.values[largest]:
                largest = left
        if right < size:
            r.comparisons += 1
            r.capture([largest, right], list(range(size, len(r.values))), "오른쪽 자식 비교")
            if r.values[right] > r.values[largest]:
                largest = right
        if largest != root:
            r.values[root], r.values[largest] = r.values[largest], r.values[root]
            r.swaps += 1
            r.capture([root, largest], list(range(size, len(r.values))), "힙 재구성")
            heapify(size, largest)

    n = len(r.values)
    # 마지막 부모 노드부터 역순으로 내려가며 전체 배열을 최대 힙으로 만듭니다.
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    # 루트의 최댓값을 끝으로 보내고, 남은 힙의 크기를 한 칸씩 줄입니다.
    for end in range(n - 1, 0, -1):
        r.values[0], r.values[end] = r.values[end], r.values[0]
        r.swaps += 1
        r.capture([0, end], list(range(end, n)), "최댓값 위치 확정")
        heapify(end, 0)


# 문자열 키와 실제 정렬 함수를 연결하여 조건문 없이 알고리즘을 선택합니다.
SORTERS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
}


def execute(algorithm: str, values: list[int], record_steps: bool = True) -> SortRecorder:
    """선택한 알고리즘을 실행하고 결과 및 기록 정보를 반환합니다."""
    recorder = SortRecorder(values, record_steps)
    SORTERS[algorithm](recorder)
    if record_steps:
        recorder.capture([], list(range(len(values))), "정렬 완료")
    return recorder


@app.get("/")
def index():
    """메인 화면에 알고리즘 메타데이터를 전달합니다."""
    return render_template("index.html", algorithms=ALGORITHM_INFO)


@app.post("/api/sort")
def sort_api():
    """입력값을 검증하고 브라우저에서 재생할 전체 정렬 단계를 반환합니다."""
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm")
    values = data.get("values")
    if algorithm not in SORTERS:
        return jsonify({"error": "지원하지 않는 알고리즘입니다."}), 400
    # 과도한 단계 데이터 생성을 막기 위해 배열 크기와 값의 범위를 제한합니다.
    if not isinstance(values, list) or not 2 <= len(values) <= 80 or not all(isinstance(v, int) and 1 <= v <= 100 for v in values):
        return jsonify({"error": "1~100 사이 정수 2~80개가 필요합니다."}), 400
    result = execute(algorithm, values)
    return jsonify({"steps": result.steps, "info": ALGORITHM_INFO[algorithm]})


@app.post("/api/benchmark")
def benchmark_api():
    """데이터 크기별 실행 시간을 세 번 측정하여 평균값을 반환합니다."""
    data = request.get_json(silent=True) or {}
    algorithms = data.get("algorithms", list(SORTERS))
    if not isinstance(algorithms, list) or any(name not in SORTERS for name in algorithms):
        return jsonify({"error": "알고리즘 목록이 올바르지 않습니다."}), 400

    sizes = [10, 25, 50, 100, 200, 400]
    series = []
    for name in algorithms:
        timings = []
        for size in sizes:
            samples = []
            for _ in range(3):
                values = [randint(1, 10_000) for _ in range(size)]
                started = perf_counter()
                # 순수 정렬 성능을 측정하기 위해 애니메이션 단계 기록은 생략합니다.
                execute(name, values, record_steps=False)
                samples.append((perf_counter() - started) * 1000)
            timings.append(round(sum(samples) / len(samples), 4))
        series.append({"key": name, "name": ALGORITHM_INFO[name]["name"], "times": timings})
    return jsonify({"sizes": sizes, "series": series})


if __name__ == "__main__":
    app.run(debug=True)
