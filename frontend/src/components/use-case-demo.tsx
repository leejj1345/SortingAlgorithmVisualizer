"use client";

import { useMemo, useState } from "react";

import type { AlgorithmUseCase, SortResponse, SortStep } from "@/types/sorting";

interface UseCaseDemoProps {
  useCase: AlgorithmUseCase;
}

const wait = (milliseconds: number) =>
  new Promise((resolve) => window.setTimeout(resolve, milliseconds));

export function UseCaseDemo({ useCase }: UseCaseDemoProps) {
  const [step, setStep] = useState<SortStep>({
    values: useCase.items.map((item) => item.value),
    active: [],
    sorted: [],
    comparisons: 0,
    swaps: 0,
    message: "시뮬레이션 준비",
  });
  const [running, setRunning] = useState(false);
  const [speed, setSpeed] = useState(260);

  const itemByValue = useMemo(
    () => new Map(useCase.items.map((item) => [item.value, item])),
    [useCase.items],
  );

  async function runSimulation() {
    setRunning(true);
    try {
      const response = await fetch("/backend/sort", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          algorithm: useCase.key,
          values: useCase.items.map((item) => item.value),
        }),
      });
      const data = (await response.json()) as SortResponse & { error?: string };
      if (!response.ok) throw new Error(data.error ?? "정렬 요청에 실패했습니다.");

      for (const nextStep of data.steps) {
        setStep(nextStep);
        await wait(speed);
      }
    } catch (error) {
      setStep((current) => ({
        ...current,
        message: error instanceof Error ? error.message : "알 수 없는 오류",
      }));
    } finally {
      setRunning(false);
    }
  }

  function reset() {
    setStep({
      values: useCase.items.map((item) => item.value),
      active: [],
      sorted: [],
      comparisons: 0,
      swaps: 0,
      message: "시뮬레이션 준비",
    });
  }

  return (
    <section className="demo-panel" style={{ "--accent": useCase.color } as React.CSSProperties}>
      <div className="demo-toolbar">
        <div>
          <span className="kicker">INTERACTIVE SCENARIO</span>
          <h2>{useCase.selectedTitle}</h2>
        </div>
        <div className="demo-actions">
          <label>
            재생 속도
            <select
              disabled={running}
              onChange={(event) => setSpeed(Number(event.target.value))}
              value={speed}
            >
              <option value={500}>느리게</option>
              <option value={260}>보통</option>
              <option value={90}>빠르게</option>
            </select>
          </label>
          <button className="button secondary" disabled={running} onClick={reset}>초기화</button>
          <button className="button accent" disabled={running} onClick={runSimulation}>
            {running ? "정렬 중…" : "사례 실행"}
          </button>
        </div>
      </div>

      <div className="domain-list" aria-live="polite">
        {step.values.map((value, index) => {
          const item = itemByValue.get(value);
          const isActive = step.active.includes(index);
          const isSorted = step.sorted.includes(index);
          return (
            <article
              className={`domain-item ${isActive ? "is-active" : ""} ${isSorted ? "is-sorted" : ""}`}
              // 삽입 정렬의 이동 단계에서는 같은 값이 잠시 두 위치에 존재할 수 있으므로
              // 값이 아닌 고정된 화면 위치를 React 목록 키로 사용합니다.
              key={index}
            >
              <span className="rank">{String(index + 1).padStart(2, "0")}</span>
              <div>
                <strong>{item?.label}</strong>
                <small>{item?.detail}</small>
              </div>
              <b>{value}</b>
            </article>
          );
        })}
      </div>

      <div className="demo-status">
        <p><span>현재 동작</span><strong>{step.message}</strong></p>
        <p><span>비교</span><strong>{step.comparisons}</strong></p>
        <p><span>교환 / 쓰기</span><strong>{step.swaps}</strong></p>
      </div>
    </section>
  );
}
