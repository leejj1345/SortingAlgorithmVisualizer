import Link from "next/link";

export default function NotFound() {
  return (
    <main className="not-found">
      <span className="kicker">404 / NOT SORTED</span>
      <h1>찾는 사례가<br />목록에 없습니다.</h1>
      <Link className="button accent" href="/">활용 사례로 돌아가기</Link>
    </main>
  );
}
