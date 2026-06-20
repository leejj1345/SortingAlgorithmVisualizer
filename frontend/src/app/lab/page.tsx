import { BenchmarkPanel } from "@/components/benchmark-panel";
import { SortLab } from "@/components/sort-lab";

export default function LabPage() {
  return (
    <main className="page-shell">
      <section className="page-hero compact">
        <span className="kicker">CLASSIC VISUALIZER</span>
        <h1>정렬 <em>실험실</em></h1>
        <p>Python 정렬 엔진의 각 단계를 Next.js 인터페이스에서 재생합니다.</p>
      </section>
      <SortLab />
      <BenchmarkPanel />
    </main>
  );
}
