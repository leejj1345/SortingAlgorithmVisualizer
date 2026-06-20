"""알고리즘 등록 정보와 패키지의 공개 실행 API를 제공합니다."""

from collections.abc import Sequence

from .algorithms import (
    SortFunction,
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from .models import SortRecorder


ALGORITHM_INFO = {
    "bubble": {"name": "Bubble Sort", "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "selection": {"name": "Selection Sort", "best": "O(n²)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "insertion": {"name": "Insertion Sort", "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)"},
    "merge": {"name": "Merge Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(n)"},
    "quick": {"name": "Quick Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)", "space": "O(log n)"},
    "heap": {"name": "Heap Sort", "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(1)"},
}


# 키 기반 레지스트리를 사용하므로 웹 UI나 다른 프로그램에서 같은 이름으로 호출할 수 있습니다.
SORTERS: dict[str, SortFunction] = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
}


def available_algorithms() -> tuple[str, ...]:
    """현재 패키지에서 사용할 수 있는 알고리즘 키를 반환합니다."""
    return tuple(SORTERS)


def sort(
    values: Sequence[int],
    algorithm: str = "quick",
    *,
    record_steps: bool = False,
) -> SortRecorder:
    """선택한 알고리즘으로 값을 정렬하고 실행 결과를 반환합니다.

    Args:
        values: 정렬할 정수 시퀀스입니다. 원본 데이터는 변경하지 않습니다.
        algorithm: ``bubble``, ``selection``, ``insertion``, ``merge``,
            ``quick``, ``heap`` 중 하나입니다.
        record_steps: True이면 시각화에 사용할 모든 실행 단계를 기록합니다.

    Raises:
        ValueError: 등록되지 않은 알고리즘 이름을 전달한 경우 발생합니다.
        TypeError: 정수가 아닌 값을 포함한 경우 발생합니다.
    """
    if algorithm not in SORTERS:
        choices = ", ".join(available_algorithms())
        raise ValueError(f"지원하지 않는 알고리즘입니다: {algorithm}. 사용 가능: {choices}")
    if any(not isinstance(value, int) for value in values):
        raise TypeError("정렬할 값은 모두 정수여야 합니다.")

    recorder = SortRecorder(list(values), record_steps=record_steps)
    SORTERS[algorithm](recorder)
    if record_steps:
        recorder.capture([], list(range(len(recorder.values))), "정렬 완료")
    return recorder
