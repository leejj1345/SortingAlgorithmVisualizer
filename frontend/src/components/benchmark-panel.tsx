"use client";

import { useState } from "react";

import { useCases } from "@/data/use-cases";

interface BenchmarkSeries {
  key: string;
  name: string;
  times: number[];
}

interface BenchmarkResponse {
  sizes: number[];
  series: BenchmarkSeries[];
  error?: string;
}

export function BenchmarkPanel() {
  const [result, setResult] = useState<BenchmarkResponse | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");

  async function runBenchmark() {
    setRunning(true);
    setError("");
    try {
      const response = await fetch("/backend/benchmark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithms: useCases.map((item) => item.key) }),
      });
      const data = (await response.json()) as BenchmarkResponse;
      if (!response.ok) throw new Error(data.error ?? "성능 측정에 실패했습니다.");
      setResult(data);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "알 수 없는 오류");
    } finally {
      setRunning(false);
    }
  }

  const maximum = result
    ? Math.max(...result.series.flatMap((series) => series.times), 0.001)
    : 1;

  return (
    <section className="benchmark-panel">
      <div className="benchmark-heading">
        <div>
          <span className="kicker">REAL PERFORMANCE</span>
          <h2>데이터가 커질 때의<br />실제 실행 시간</h2>
          <p>Python 엔진에서 각 크기를 세 번 실행한 평균값입니다.</p>
        </div>
        <button className="button accent" disabled={running} onClick={runBenchmark}>
          {running ? "측정 중…" : result ? "다시 측정" : "성능 측정"}
        </button>
      </div>

      {error && <p className="benchmark-error">{error}</p>}
      {!result && !error && <div className="benchmark-empty">측정 버튼을 누르면 10~400개 데이터의 결과가 나타납니다.</div>}
      {result && (
        <div className="benchmark-chart" role="img" aria-label="알고리즘별 데이터 크기 실행 시간 그래프">
          <div className="size-axis">
            <span>알고리즘</span>
            {result.sizes.map((size) => <span key={size}>{size}개</span>)}
          </div>
          {result.series.map((series) => {
            const color = useCases.find((item) => item.key === series.key)?.color;
            return (
              <div className="performance-row" key={series.key}>
                <strong>{series.name}</strong>
                {series.times.map((time, index) => (
                  <div className="performance-cell" key={`${series.key}-${result.sizes[index]}`}>
                    <i style={{ width: `${Math.max((time / maximum) * 100, 2)}%`, background: color }} />
                    <span>{time.toFixed(3)}ms</span>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
