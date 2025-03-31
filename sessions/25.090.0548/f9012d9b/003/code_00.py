import numpy as np
from collections import Counter

"""
Transforms an input grid based on the frequency and properties of its non-white colors.

1.  Identify all unique non-white colors (pixels != 0) and their frequencies.
2.  If no non-white colors exist, return a 1x1 white (0) grid.
3.  Sort colors by frequency (descending), then value (ascending).
4.  If only one unique non-white color `c` exists, return `[[c]]`.
5.  Determine the most frequent color (`c1`) and its count (`count1`).
6.  If `count1 < 10`:
    - Find the least frequent color (`c_least`).
    - Return `[[c_least]]`.
7.  If `count1 >= 10`:
    - Find the second most frequent color (`c2`).
    - Check the parity of `c1`.
    - If `c1` is odd, return `[[c1, c1], [c2, c1]]`.
    - If `c1` is even, return `[[c2, c2], [c2, c1]]`.
"""


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rules based on color frequencies and parity.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid (either 1x1 or 2x2).
    """

    # 1. Flatten input grid, remove white pixels (0).
    pixels = input_grid.flatten()
    non_white_pixels = [p for p in pixels if p != 0]

    # 2. If no non-white pixels, return a 1x1 white (0) grid.
    if not non_white_pixels:
        return np.array([[0]], dtype=int)

    # 3. Count frequencies of remaining pixels.
    color_counts = Counter(non_white_pixels)

    # 4. Sort colors by frequency descending, then color value ascending.
    #    Ensure keys are integers for sorting, not numpy types if Counter yields them.
    sorted_counts = sorted(color_counts.items(), key=lambda item: (-item[1], int(item[0])))

    # 5. If only one unique non-white color `c` exists, return `[[c]]`.
    if len(sorted_counts) == 1:
        c1, _ = sorted_counts[0]
        output_grid = np.array([[c1]], dtype=int)
        return output_grid

    # 6. Determine the most frequent color (`c1`) and its count (`count1`).
    c1, count1 = sorted_counts[0]
    # Ensure c1 is a standard python int for modulo operation
    c1 = int(c1) 

    # Check the threshold condition
    if count1 < 10:
        # 6.a Find the least frequent color (`c_least`).
        c_least, _ = sorted_counts[-1]
        # 6.b Return `[[c_least]]`.
        output_grid = np.array([[c_least]], dtype=int)
    else:
        # 7. `count1 >= 10` case
        # 7.a Find the second most frequent color (`c2`).
        c2, _ = sorted_counts[1]
        # Ensure c2 is a standard python int
        c2 = int(c2) 

        # 7.b Create a 2x2 output grid, initialized with zeros (or any value)
        output_grid = np.zeros((2, 2), dtype=int)

        # 7.c Check the parity of `c1`.
        if c1 % 2 != 0:  # c1 is odd
            # 7.d If `c1` is odd, return `[[c1, c1], [c2, c1]]`.
            output_grid[0, 0] = c1
            output_grid[0, 1] = c1
            output_grid[1, 0] = c2
            output_grid[1, 1] = c1
        else:  # c1 is even
            # 7.e If `c1` is even, return `[[c2, c2], [c2, c1]]`.
            output_grid[0, 0] = c2
            output_grid[0, 1] = c2
            output_grid[1, 0] = c2
            output_grid[1, 1] = c1

    return output_grid