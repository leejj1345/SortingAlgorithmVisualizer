import { UseCasePage } from "@/components/use-case-page";
import { useCaseMap } from "@/data/use-cases";

/** 병합 정렬: 다중 배송 로그 병합 활용 페이지 */
export default function MergeUseCasePage() {
  return <UseCasePage useCase={useCaseMap.merge} />;
}
