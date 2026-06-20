from __future__ import annotations

from random import randint
from time import perf_counter

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


ALGORITHM_INFO = {
    "bubble": {"name": "Bubble Sort", "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "selection": {"name": "Selection Sort", "best": "O(n²)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "insertion": {"name": "Insertion Sort", "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "merge": {"name": "Merge Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(n)"},
    "quick": {"name": "Quick Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)", "space": "O(log n)"},
    "heap": {"name": "Heap Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(1)"},
}


class SortRecorder:
    def __init__(self, values: list[int], record_steps: bool = True):
        self.values = values[:]
        self.comparisons = 0
        self.swaps = 0
        self.steps: list[dict] = []
        self.record_steps = record_steps
        if record_steps:
            self.capture([], [], "준비")

    def capture(self, active: list[int], sorted_indices: list[int] | None = None, message: str = "") -> None:
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
    n = len(r.values)
    for end in range(n - 1, 0, -1):
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
    for i in range(1, len(r.values)):
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
    def merge(left: int, mid: int, right: int) -> None:
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
        if left >= right:
            return
        mid = (left + right) // 2
        divide(left, mid)
        divide(mid + 1, right)
        merge(left, mid, right)

    divide(0, len(r.values) - 1)


def quick_sort(r: SortRecorder) -> None:
    def partition(low: int, high: int) -> int:
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
    def heapify(size: int, root: int) -> None:
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
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for end in range(n - 1, 0, -1):
        r.values[0], r.values[end] = r.values[end], r.values[0]
        r.swaps += 1
        r.capture([0, end], list(range(end, n)), "최댓값 위치 확정")
        heapify(end, 0)


SORTERS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
}


def execute(algorithm: str, values: list[int], record_steps: bool = True) -> SortRecorder:
    recorder = SortRecorder(values, record_steps)
    SORTERS[algorithm](recorder)
    if record_steps:
        recorder.capture([], list(range(len(values))), "정렬 완료")
    return recorder


@app.get("/")
def index():
    return render_template("index.html", algorithms=ALGORITHM_INFO)


@app.post("/api/sort")
def sort_api():
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm")
    values = data.get("values")
    if algorithm not in SORTERS:
        return jsonify({"error": "지원하지 않는 알고리즘입니다."}), 400
    if not isinstance(values, list) or not 2 <= len(values) <= 80 or not all(isinstance(v, int) and 1 <= v <= 100 for v in values):
        return jsonify({"error": "1~100 사이 정수 2~80개가 필요합니다."}), 400
    result = execute(algorithm, values)
    return jsonify({"steps": result.steps, "info": ALGORITHM_INFO[algorithm]})


@app.post("/api/benchmark")
def benchmark_api():
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
                execute(name, values, record_steps=False)
                samples.append((perf_counter() - started) * 1000)
            timings.append(round(sum(samples) / len(samples), 4))
        series.append({"key": name, "name": ALGORITHM_INFO[name]["name"], "times": timings})
    return jsonify({"sizes": sizes, "series": series})


if __name__ == "__main__":
    app.run(debug=True)
