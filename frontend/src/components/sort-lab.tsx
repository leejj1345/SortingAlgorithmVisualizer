"use client";

import { useMemo, useRef, useState } from "react";

import { useCases } from "@/data/use-cases";
import type { AlgorithmKey, SortResponse, SortStep } from "@/types/sorting";

const emptyStep = (values: number[]): SortStep => ({
  values,
  active: [],
  sorted: [],
  comparisons: 0,
  swaps: 0,
  message: "준비",
});

// 서버 렌더링과 브라우저 hydration 결과가 같도록 첫 화면은 고정 데이터를 사용합니다.
const INITIAL_VALUES = [62, 12, 89, 88, 20, 79, 85, 15, 68, 64, 19, 52, 56, 72, 25, 81, 58, 31];

export function SortLab() {
  const [algorithm, setAlgorithm] = useState<AlgorithmKey>("bubble");
  const [size, setSize] = useState(18);
  const [speed, setSpeed] = useState(140);
  const [step, setStep] = useState<SortStep>(() => emptyStep(INITIAL_VALUES));
  const [running, setRunning] = useState(false);
  const [paused, setPaused] = useState(false);
  const token = useRef(0);

  const activeInfo = useMemo(
    () => useCases.find((item) => item.key === algorithm)!,
    [algorithm],
  );

  function randomize(nextSize = size) {
    token.current += 1;
    setRunning(false);
    setPaused(false);
    setStep(emptyStep(makeValues(nextSize)));
  }

  async function start() {
    const currentToken = ++token.current;
    setRunning(true);
    setPaused(false);
    try {
      const response = await fetch("/backend/sort", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithm, values: step.values }),
      });
      const data = (await response.json()) as SortResponse & { error?: string };
      if (!response.ok) throw new Error(data.error ?? "정렬 요청에 실패했습니다.");
      for (const nextStep of data.steps) {
        if (token.current !== currentToken) return;
        while (pausedState.current) await sleep(60);
        setStep(nextStep);
        await sleep(speed);
      }
    } catch (error) {
      setStep((current) => ({
        ...current,
        message: error instanceof Error ? error.message : "알 수 없는 오류",
      }));
    } finally {
      if (token.current === currentToken) setRunning(false);
    }
  }

  const pausedState = useRef(false);
  function togglePause() {
    pausedState.current = !pausedState.current;
    setPaused(pausedState.current);
  }

  return (
    <section className="lab-shell" style={{ "--accent": activeInfo.color } as React.CSSProperties}>
      <div className="lab-controls">
        <label>
          알고리즘
          <select disabled={running} value={algorithm} onChange={(event) => setAlgorithm(event.target.value as AlgorithmKey)}>
            {useCases.map((item) => <option key={item.key} value={item.key}>{item.name}</option>)}
          </select>
        </label>
        <label>
          데이터 <b>{size}</b>
          <input
            disabled={running}
            max={50}
            min={5}
            onChange={(event) => {
              const nextSize = Number(event.target.value);
              setSize(nextSize);
              randomize(nextSize);
            }}
            type="range"
            value={size}
          />
        </label>
        <label>
          속도
          <select disabled={running} value={speed} onChange={(event) => setSpeed(Number(event.target.value))}>
            <option value={400}>0.5×</option>
            <option value={140}>1.0×</option>
            <option value={35}>2.0×</option>
          </select>
        </label>
        <div className="lab-actions">
          <button className="button secondary" disabled={running} onClick={() => randomize()}>새 데이터</button>
          <button className="button accent" disabled={running} onClick={start}>정렬 시작</button>
          <button className="button secondary" disabled={!running} onClick={togglePause}>{paused ? "계속" : "정지"}</button>
        </div>
      </div>

      <div className="bars-area">
        <div className="bars-message"><span>{activeInfo.badge}</span><strong>{step.message}</strong></div>
        <div className="bars">
          {step.values.map((value, index) => (
            <div
              className={`bar ${step.active.includes(index) ? "active" : ""} ${step.sorted.includes(index) ? "sorted" : ""}`}
              key={`${index}-${value}`}
              style={{ height: `${value}%` }}
              title={String(value)}
            />
          ))}
        </div>
      </div>

      <div className="lab-metrics">
        <p><span>비교 횟수</span><strong>{step.comparisons}</strong></p>
        <p><span>교환 / 쓰기</span><strong>{step.swaps}</strong></p>
        <p><span>평균 복잡도</span><strong>{activeInfo.complexity.average}</strong></p>
        <p><span>상태</span><strong>{running ? (paused ? "PAUSED" : "RUNNING") : "READY"}</strong></p>
      </div>
    </section>
  );
}

function makeValues(size: number) {
  return Array.from({ length: size }, () => Math.floor(Math.random() * 84) + 10);
}

function sleep(milliseconds: number) {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}
