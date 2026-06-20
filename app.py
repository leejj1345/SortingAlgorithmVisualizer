"""Sort Lab의 Flask 웹 애플리케이션 진입점입니다.

정렬 로직은 독립적인 ``sorting`` 패키지에 있으며, 이 모듈은 HTTP 요청과
정렬 엔진 사이를 연결하는 웹 어댑터 역할만 담당합니다.
"""

from random import randint
from time import perf_counter

from flask import Flask, jsonify, request

from sorting import ALGORITHM_INFO, SORTERS, sort


app = Flask(__name__)


@app.get("/")
def index():
    """API 서버 상태와 Next.js 프런트엔드 주소를 반환합니다."""
    return jsonify(
        {
            "service": "SORT LAB API",
            "status": "ok",
            "frontend": "http://localhost:3000",
            "algorithms": list(SORTERS),
        }
    )


@app.post("/api/sort")
def sort_api():
    """입력값을 검증하고 브라우저에서 재생할 전체 정렬 단계를 반환합니다."""
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm")
    values = data.get("values")

    if algorithm not in SORTERS:
        return jsonify({"error": "지원하지 않는 알고리즘입니다."}), 400

    # 과도한 단계 데이터 생성을 막기 위해 배열 크기와 값의 범위를 제한합니다.
    if not isinstance(values, list) or not 2 <= len(values) <= 80 or not all(
        isinstance(value, int) and 1 <= value <= 100 for value in values
    ):
        return jsonify({"error": "1~100 사이 정수 2~80개가 필요합니다."}), 400

    result = sort(values, algorithm=algorithm, record_steps=True)
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
                sort(values, algorithm=name, record_steps=False)
                samples.append((perf_counter() - started) * 1000)
            timings.append(round(sum(samples) / len(samples), 4))

        series.append({"key": name, "name": ALGORITHM_INFO[name]["name"], "times": timings})

    return jsonify({"sizes": sizes, "series": series})


if __name__ == "__main__":
    app.run(debug=True)
