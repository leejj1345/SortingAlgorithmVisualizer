import { UseCasePage } from "@/components/use-case-page";
import { useCaseMap } from "@/data/use-cases";

/** 힙 정렬: 긴급 작업 스케줄러 활용 페이지 */
export default function HeapUseCasePage() {
  return <UseCasePage useCase={useCaseMap.heap} />;
}
