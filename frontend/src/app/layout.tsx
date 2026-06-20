import type { Metadata } from "next";

import { AppHeader } from "@/components/app-header";

import "./globals.css";

export const metadata: Metadata = {
  title: "SORT LAB — 알고리즘 활용 스튜디오",
  description: "정렬 알고리즘의 원리와 실제 활용 분야를 인터랙티브하게 탐색합니다.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>
        <AppHeader />
        {children}
        <footer className="site-footer">
          <span>SORT LAB / NEXT.JS + FLASK</span>
          <span>ALGORITHMS IN CONTEXT</span>
        </footer>
      </body>
    </html>
  );
}
