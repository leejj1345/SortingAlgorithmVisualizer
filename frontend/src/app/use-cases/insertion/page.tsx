import { UseCasePage } from "@/components/use-case-page";
import { useCaseMap } from "@/data/use-cases";

/** 삽입 정렬: 실시간 이벤트 타임라인 활용 페이지 */
export default function InsertionUseCasePage() {
  return <UseCasePage useCase={useCaseMap.insertion} />;
}
