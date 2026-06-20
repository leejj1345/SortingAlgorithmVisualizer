"""SortRecorder를 공통 인터페이스로 사용하는 정렬 알고리즘 구현 모음입니다."""

from collections.abc import Callable

from .models import SortRecorder


SortFunction = Callable[[SortRecorder], None]


def bubble_sort(recorder: SortRecorder) -> None:
    """인접 원소를 비교하여 큰 값을 배열 오른쪽부터 확정합니다."""
    values = recorder.values
    for end in range(len(values) - 1, 0, -1):
        changed = False
        for index in range(end):
            recorder.comparisons += 1
            recorder.capture([index, index + 1], list(range(end + 1, len(values))), "인접 원소 비교")
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                recorder.swaps += 1
                changed = True
                recorder.capture([index, index + 1], list(range(end + 1, len(values))), "교환")
        # 한 회전에서 교환이 없다면 이미 정렬된 상태입니다.
        if not changed:
            break


def selection_sort(recorder: SortRecorder) -> None:
    """정렬되지 않은 구간의 최솟값을 찾아 앞쪽에 배치합니다."""
    values = recorder.values
    for index in range(len(values) - 1):
        minimum = index
        for cursor in range(index + 1, len(values)):
            recorder.comparisons += 1
            recorder.capture([minimum, cursor], list(range(index)), "최솟값 탐색")
            if values[cursor] < values[minimum]:
                minimum = cursor
        if minimum != index:
            values[index], values[minimum] = values[minimum], values[index]
            recorder.swaps += 1
            recorder.capture([index, minimum], list(range(index)), "최솟값을 앞으로 이동")


def insertion_sort(recorder: SortRecorder) -> None:
    """현재 값을 왼쪽의 정렬된 구간에서 알맞은 위치에 삽입합니다."""
    values = recorder.values
    for index in range(1, len(values)):
        key = values[index]
        cursor = index - 1
        while cursor >= 0:
            recorder.comparisons += 1
            recorder.capture([cursor, cursor + 1], list(range(index)), "삽입 위치 비교")
            if values[cursor] <= key:
                break
            values[cursor + 1] = values[cursor]
            recorder.swaps += 1
            recorder.capture([cursor, cursor + 1], [], "오른쪽으로 이동")
            cursor -= 1
        values[cursor + 1] = key


def merge_sort(recorder: SortRecorder) -> None:
    """배열을 재귀적으로 분할한 뒤 정렬된 두 부분 배열을 병합합니다."""
    values = recorder.values

    def merge(left: int, middle: int, right: int) -> None:
        left_values = values[left : middle + 1]
        right_values = values[middle + 1 : right + 1]
        left_index = right_index = 0
        target = left

        while left_index < len(left_values) and right_index < len(right_values):
            recorder.comparisons += 1
            recorder.capture([left + left_index, middle + 1 + right_index], [], "두 부분 배열 비교")
            if left_values[left_index] <= right_values[right_index]:
                values[target] = left_values[left_index]
                left_index += 1
            else:
                values[target] = right_values[right_index]
                right_index += 1
            # 병합 정렬은 교환 대신 원본 배열에 값을 쓴 횟수를 집계합니다.
            recorder.swaps += 1
            recorder.capture([target], [], "병합하여 쓰기")
            target += 1

        while left_index < len(left_values):
            values[target] = left_values[left_index]
            recorder.swaps += 1
            recorder.capture([target], [], "남은 원소 쓰기")
            left_index += 1
            target += 1

        while right_index < len(right_values):
            values[target] = right_values[right_index]
            recorder.swaps += 1
            recorder.capture([target], [], "남은 원소 쓰기")
            right_index += 1
            target += 1

    def divide(left: int, right: int) -> None:
        if left >= right:
            return
        middle = (left + right) // 2
        divide(left, middle)
        divide(middle + 1, right)
        merge(left, middle, right)

    divide(0, len(values) - 1)


def quick_sort(recorder: SortRecorder) -> None:
    """마지막 원소를 피벗으로 사용하는 Lomuto 방식의 퀵 정렬입니다."""
    values = recorder.values

    def partition(low: int, high: int) -> int:
        pivot_value = values[high]
        boundary = low
        for cursor in range(low, high):
            recorder.comparisons += 1
            recorder.capture([cursor, high], [], f"피벗 {pivot_value}과 비교")
            if values[cursor] <= pivot_value:
                if boundary != cursor:
                    values[boundary], values[cursor] = values[cursor], values[boundary]
                    recorder.swaps += 1
                    recorder.capture([boundary, cursor], [], "피벗보다 작은 값 이동")
                boundary += 1
        if boundary != high:
            values[boundary], values[high] = values[high], values[boundary]
            recorder.swaps += 1
            recorder.capture([boundary, high], [], "피벗 위치 확정")
        return boundary

    def divide(low: int, high: int) -> None:
        if low < high:
            pivot = partition(low, high)
            divide(low, pivot - 1)
            divide(pivot + 1, high)

    divide(0, len(values) - 1)


def heap_sort(recorder: SortRecorder) -> None:
    """최대 힙을 구성하고 최댓값을 배열 뒤쪽부터 확정합니다."""
    values = recorder.values

    def heapify(size: int, root: int) -> None:
        largest = root
        left = root * 2 + 1
        right = root * 2 + 2

        if left < size:
            recorder.comparisons += 1
            recorder.capture([largest, left], list(range(size, len(values))), "왼쪽 자식 비교")
            if values[left] > values[largest]:
                largest = left
        if right < size:
            recorder.comparisons += 1
            recorder.capture([largest, right], list(range(size, len(values))), "오른쪽 자식 비교")
            if values[right] > values[largest]:
                largest = right
        if largest != root:
            values[root], values[largest] = values[largest], values[root]
            recorder.swaps += 1
            recorder.capture([root, largest], list(range(size, len(values))), "힙 재구성")
            heapify(size, largest)

    size = len(values)
    for index in range(size // 2 - 1, -1, -1):
        heapify(size, index)
    for end in range(size - 1, 0, -1):
        values[0], values[end] = values[end], values[0]
        recorder.swaps += 1
        recorder.capture([0, end], list(range(end, size)), "최댓값 위치 확정")
        heapify(end, 0)
