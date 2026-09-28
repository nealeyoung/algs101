#!/usr/bin/env python3


class Subarray:
    def __init__(self, array: list[list[float]], i_range: range, j_range: range) -> None:
        """array is a list of lists; i_range and j_range are ranges"""
        self.array = array
        self.i_range = i_range
        self.j_range = j_range

    def find_nbr_larger_than(self, i: int, j: int) -> tuple[int, int] | None:
        """
        return neighboring cell in subarray with larger value,
        or None if there is no such cell
        """
        for i2, j2 in ((i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1)):
            if i2 in self.i_range and j2 in self.j_range and self.array[i2][j2] > self.array[i][j]:
                return i2, j2
        return None

    def find_local_max(self) -> tuple[int, int]:
        def partition(range_: range) -> tuple[range, int, range]:
            mid = int(len(range_) / 2)
            return range_[:mid], range_[mid], range_[mid + 1 :]

        top, mid_i, bottom = partition(self.i_range)
        left, mid_j, right = partition(self.j_range)

        middle_row = set((mid_i, j) for j in self.j_range)
        middle_col = set((i, mid_j) for i in self.i_range)
        cross = sorted(middle_row | middle_col)

        for i, j in cross:
            if self.find_nbr_larger_than(i, j) is None:
                return i, j

        i, j = max(cross, key=lambda ij: self.array[ij[0]][ij[1]])

        i2, j2 = self.find_nbr_larger_than(i, j)  # type: ignore[misc] # not None, see loop above
        i2_range = top if i2 in top else bottom
        j2_range = left if j2 in left else right

        return Subarray(self.array, i2_range, j2_range).find_local_max()

    @staticmethod
    def from_string(input_: str) -> "Subarray":
        """input_: array as string.  output: array as Subarray"""
        try:
            array = [
                [float(x.strip()) for x in line.strip().split() if x.strip()]
                for line in input_.split("\n")
                if line.strip()
            ]
            if not array:
                raise ValueError
            m, n = len(array), len(array[0])
            if not (m and n and all(len(row) == n for row in array)):
                raise ValueError
            return Subarray(array, range(m), range(n))

        except ValueError as e:
            raise AssertionError("MALFORMED INPUT") from e


if __name__ == "__main__":

    def main(input_: str) -> None:
        A = Subarray.from_string(input_)
        i, j = A.find_local_max()
        if A.find_nbr_larger_than(i, j) is None:
            print("local max:", i, j, "; value:", A.array[i][j])
        else:
            print("NOT LOCAL MAX:", i, j, "; value:", A.array[i][j])

    input_1 = """
     0 1 3
     3 2 3
     2 5 0
    """

    main(input_1)

    input_2 = """
    3 2 2
    2 2 1
    2 1 0
    """

    main(input_2)
