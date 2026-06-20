import { UseCasePage } from "@/components/use-case-page";
import { useCaseMap } from "@/data/use-cases";

/** 선택 정렬: 쇼핑몰 최저가 탐색 활용 페이지 */
export default function SelectionUseCasePage() {
  return <UseCasePage useCase={useCaseMap.selection} />;
}
