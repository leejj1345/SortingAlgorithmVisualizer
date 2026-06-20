import Link from "next/link";

export function AppHeader() {
  return (
    <header className="site-header">
      <Link className="brand" href="/">
        <span className="brand-mark">S</span>
        <span>SORT LAB</span>
      </Link>
      <nav aria-label="주요 메뉴">
        <Link href="/">활용 사례</Link>
        <Link href="/lab">정렬 실험실</Link>
      </nav>
    </header>
  );
}
