import Link from "next/link";

import { useCases } from "@/data/use-cases";

export default function HomePage() {
  return (
    <main>
      <section className="home-hero">
        <div>
          <span className="kicker">ALGORITHMS IN THE REAL WORLD</span>
          <h1>정렬은 어디에<br /><em>쓰일까요?</em></h1>
        </div>
        <div className="hero-note">
          <p>여섯 알고리즘을 실제 문제에 연결했습니다. 후보를 비교하고, 선정한 사례를 직접 실행해 보세요.</p>
          <Link className="text-link" href="/lab">기본 정렬 실험실 열기 →</Link>
        </div>
      </section>

      <section className="selection-intro">
        <span className="kicker">6 ALGORITHMS · 18 CANDIDATES</span>
        <h2>알고리즘마다<br />잘하는 일이 다릅니다.</h2>
      </section>

      <section className="case-grid">
        {useCases.map((item, index) => (
          <article className="case-card" key={item.key} style={{ "--accent": item.color } as React.CSSProperties}>
            <div className="case-number">0{index + 1}</div>
            <div className="case-heading">
              <span>{item.badge}</span>
              <h3>{item.name}</h3>
              <p>{item.koreanName}</p>
            </div>
            <p className="case-summary">{item.summary}</p>
            <div className="candidate-preview">
              {item.candidates.map((candidate) => (
                <div className={candidate.fit === "선정" ? "selected" : ""} key={candidate.title}>
                  <span>{candidate.fit}</span>
                  <strong>{candidate.title}</strong>
                </div>
              ))}
            </div>
            <Link className="card-link" href={`/use-cases/${item.key}`}>사례 페이지 보기 <span>↗</span></Link>
          </article>
        ))}
      </section>
    </main>
  );
}
