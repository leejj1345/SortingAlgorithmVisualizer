"""정렬 결과와 시각화 단계에 사용하는 공통 데이터 모델입니다."""

from __future__ import annotations

from typing import TypedDict


class SortStep(TypedDict):
    """프런트엔드가 한 프레임을 렌더링하는 데 필요한 데이터 형식입니다."""

    values: list[int]
    active: list[int]
    sorted: list[int]
    comparisons: int
    swaps: int
    message: str


class SortRecorder:
    """정렬 결과와 비교·교환 횟수, 선택적 실행 단계를 기록합니다.

    전달받은 배열을 복사하므로 호출자의 원본 데이터는 변경되지 않습니다.
    ``record_steps=False``를 사용하면 시각화 프레임을 만들지 않아 벤치마크나
    일반 정렬 용도로 더 가볍게 사용할 수 있습니다.
    """

    def __init__(self, values: list[int], record_steps: bool = False) -> None:
        self.values = values[:]
        self.comparisons = 0
        self.swaps = 0
        self.steps: list[SortStep] = []
        self.record_steps = record_steps

        if record_steps:
            self.capture([], [], "준비")

    def capture(
        self,
        active: list[int],
        sorted_indices: list[int] | None = None,
        message: str = "",
    ) -> None:
        """현재 배열과 강조할 인덱스를 하나의 애니메이션 프레임으로 저장합니다."""
        if not self.record_steps:
            return

        self.steps.append(
            {
                "values": self.values[:],
                "active": active[:],
                "sorted": (sorted_indices or [])[:],
                "comparisons": self.comparisons,
                "swaps": self.swaps,
                "message": message,
            }
        )
