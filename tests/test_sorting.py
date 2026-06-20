"""웹 프레임워크와 독립적으로 정렬 패키지를 검증합니다."""

import unittest

from sorting import available_algorithms, sort


class SortingPackageTests(unittest.TestCase):
    def test_all_algorithms_sort_without_changing_source(self) -> None:
        source = [8, 3, 5, 1, 9, 2, 3]
        expected = sorted(source)

        for algorithm in available_algorithms():
            with self.subTest(algorithm=algorithm):
                result = sort(source, algorithm=algorithm)
                self.assertEqual(result.values, expected)
                self.assertEqual(source, [8, 3, 5, 1, 9, 2, 3])

    def test_step_recording_is_optional(self) -> None:
        self.assertEqual(sort([2, 1], record_steps=False).steps, [])
        self.assertGreater(len(sort([2, 1], record_steps=True).steps), 0)

    def test_unknown_algorithm_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            sort([2, 1], algorithm="unknown")

    def test_non_integer_value_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            sort([2, "1"], algorithm="quick")  # type: ignore[list-item]


if __name__ == "__main__":
    unittest.main()
