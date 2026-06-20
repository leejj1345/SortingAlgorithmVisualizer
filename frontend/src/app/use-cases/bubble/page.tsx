import { UseCasePage } from "@/components/use-case-page";
import { useCaseMap } from "@/data/use-cases";

/** 버블 정렬: 소규모 실시간 순위표 활용 페이지 */
export default function BubbleUseCasePage() {
  return <UseCasePage useCase={useCaseMap.bubble} />;
}
