import Link from "next/link";

import { UseCaseDemo } from "@/components/use-case-demo";
import { useCases } from "@/data/use-cases";
import type { AlgorithmUseCase } from "@/types/sorting";

interface UseCasePageProps {
  useCase: AlgorithmUseCase;
}

/** 알고리즘별 페이지가 공유하는 후보 비교 및 시뮬레이션 레이아웃입니다. */
export function UseCasePage({ useCase }: UseCasePageProps) {
  return (
    <main className="page-shell">
      <section className="use-case-hero" style={{ "--accent": useCase.color } as React.CSSProperties}>
        <div>
          <Link className="back-link" href="/">← 전체 활용 사례</Link>
          <span className="kicker">{useCase.badge}</span>
          <h1>{useCase.koreanName}<br /><em>{useCase.selectedTitle}</em></h1>
        </div>
        <div className="hero-facts">
          <p>{useCase.summary}</p>
          <dl>
            <div><dt>평균 시간</dt><dd>{useCase.complexity.average}</dd></div>
            <div><dt>공간</dt><dd>{useCase.complexity.space}</dd></div>
            <div><dt>안정 정렬</dt><dd>{useCase.complexity.stable}</dd></div>
          </dl>
        </div>
      </section>

      <section className="candidate-section">
        <div className="section-heading">
          <span className="kicker">CANDIDATE REVIEW</span>
          <h2>활용 후보 3가지</h2>
        </div>
        <div className="candidate-grid">
          {useCase.candidates.map((candidate, index) => (
            <article className={candidate.fit === "선정" ? "chosen" : ""} key={candidate.title}>
              <span>0{index + 1} / {candidate.fit}</span>
              <h3>{candidate.title}</h3>
              <p>{candidate.description}</p>
            </article>
          ))}
        </div>
        <div className="decision-note">
          <span>선정 이유</span>
          <p>{useCase.selectedReason}</p>
        </div>
      </section>

      <UseCaseDemo useCase={useCase} />

      <nav className="algorithm-nav" aria-label="다른 알고리즘 사례">
        {useCases.map((item) => (
          <Link className={item.key === useCase.key ? "current" : ""} href={`/use-cases/${item.key}`} key={item.key}>
            {item.name}
          </Link>
        ))}
      </nav>
    </main>
  );
}
