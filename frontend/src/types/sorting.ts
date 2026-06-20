export type AlgorithmKey =
  | "bubble"
  | "selection"
  | "insertion"
  | "merge"
  | "quick"
  | "heap";

export interface SortStep {
  values: number[];
  active: number[];
  sorted: number[];
  comparisons: number;
  swaps: number;
  message: string;
}

export interface SortResponse {
  steps: SortStep[];
  info: {
    name: string;
    best: string;
    average: string;
    worst: string;
    space: string;
  };
}

export interface DomainItem {
  label: string;
  value: number;
  detail: string;
}

export interface UseCaseCandidate {
  title: string;
  description: string;
  fit: string;
}

export interface AlgorithmUseCase {
  key: AlgorithmKey;
  name: string;
  koreanName: string;
  badge: string;
  color: string;
  summary: string;
  selectedTitle: string;
  selectedReason: string;
  metricLabel: string;
  order: "asc";
  candidates: UseCaseCandidate[];
  items: DomainItem[];
  complexity: {
    average: string;
    space: string;
    stable: string;
  };
}
