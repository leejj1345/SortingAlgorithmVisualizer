import { UseCasePage } from "@/components/use-case-page";
import { useCaseMap } from "@/data/use-cases";

/** 퀵 정렬: 상품 가격 카탈로그 활용 페이지 */
export default function QuickUseCasePage() {
  return <UseCasePage useCase={useCaseMap.quick} />;
}
