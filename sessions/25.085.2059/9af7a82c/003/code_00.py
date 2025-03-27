"""
Transforms an input grid into a vertical histogram representing the frequency of each non-white color.

1.  Scan the input grid and count the occurrences (frequency) of each non-white pixel color (values 1 through 9). Ignore white pixels (value 0).
2.  Identify the set of unique non-white colors present and their corresponding frequencies.
3.  Determine the maximum frequency (`MaxCount`) among all counted colors. If no non-white colors are present, `MaxCount` is 0.
4.  Determine the number of unique non-white colors found (`UniqueColorCount`).
5.  Calculate the dimensions for the output grid:
    *   Height (`H_out`) = `MaxCount`.
    *   Width (`W_out`) = `UniqueColorCount`.
6.  Create a new grid with dimensions `H_out` x `W_out`, initially filled entirely with the white color (0).
7.  Sort the unique non-white colors based primarily on their frequencies in descending order. As a secondary sorting criterion (for ties in frequency), sort by the color value itself in ascending order.
8.  Iterate through the sorted colors. For each color, assign it to a column in the output grid, starting with the leftmost column (index 0) for the first color in the sorted list (the most frequent), the next column (index 1) for the second color, and so on.
9.  For each assigned column `c` and its corresponding color `val` with frequency `count`, fill the cells from row 0 down to row `count - 1` in that column `c` with the color `val`.
10. Return the resulting output grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms an input grid into an output grid representing a histogram
    of non-white color frequencies.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output histogram grid.
    """

    # 1. Scan the input grid to count frequencies of non-white colors
    pixels = input_grid.flatten()
    color_counts = Counter(int(p) for p in pixels if p != 0) # Ensure keys are standard ints

    # 2. Identify unique colors and their counts (already done by Counter)

    # 4. Determine the number of unique non-white colors (output width)
    unique_color_count = len(color_counts)
    w_out = unique_color_count

    # 3. Determine the maximum frequency (output height)
    max_count = 0
    if color_counts:
        max_count = max(color_counts.values())
    h_out = max_count

    # 5. Output grid dimensions are H_out x W_out

    # Handle edge case: If no non-white colors, return an empty grid (0x0)
    # If h_out is 0 or w_out is 0, the grid should be empty or have 0 size in one dimension.
    # np.zeros handles dimensions like (0, N) or (N, 0) correctly, resulting in arrays with shape (0, N) or (N, 0).
    # A shape of (0, 0) is also valid.
    
    # 6. Create a new grid with dimensions H_out x W_out, filled with white (0)
    output_grid = np.zeros((h_out, w_out), dtype=int)

    # If there are no colors to plot, return the empty/zero grid now
    if w_out == 0:
        return output_grid

    # 7. Sort colors: frequency descending (primary), color value ascending (secondary)
    # The key uses a tuple: (-count, color). Negative count sorts descending.
    sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))

    # 8. Iterate through sorted colors and assign to columns
    for col_idx, (color, count) in enumerate(sorted_colors):
        # 9. Fill the column from top (row 0) down to row count - 1
        if count > 0: # Ensure count is positive
             # Fill height is simply the count, as the grid height (h_out) is max_count.
             # No need to check against h_out because count <= max_count by definition.
             output_grid[0:count, col_idx] = color

    # 10. Return the resulting grid
    return output_grid