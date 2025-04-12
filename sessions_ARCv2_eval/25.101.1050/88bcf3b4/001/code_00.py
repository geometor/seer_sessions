import numpy as np
from collections import Counter

"""
The transformation identifies two target columns in the output grid based on the overall distribution of non-background pixels in the input grid. 
Specifically, it finds the rightmost column index ('max_col') containing any non-background pixel and the second rightmost column index ('col_R2') containing any non-background pixel.
It then iterates through each row of the input grid. For each row, it finds the non-background pixels. 
The color of the rightmost non-background pixel in the input row is placed in the corresponding row of the output grid at column 'max_col'.
If there is a second rightmost non-background pixel in the input row, its color is placed in the corresponding row of the output grid at column 'col_R2'.
The rest of the output grid is filled with the background color, which is the most frequent color in the input grid.
"""

def find_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid, assumed to be the background."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default background if grid is empty
    # Common case: most frequent is background
    # Handle cases where the background might not be the absolute most frequent
    # But typically in ARC, the background (often 0) dominates.
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_target_columns(grid: np.ndarray, background_color: int) -> tuple[int | None, int | None]:
    """
    Finds the indices of the rightmost and second rightmost columns
    containing non-background pixels.
    Returns (max_col, col_R2). Returns None for an index if not found.
    """
    rows, cols = grid.shape
    non_bg_cols = set()
    for c in range(cols):
        if np.any(grid[:, c] != background_color):
            non_bg_cols.add(c)

    sorted_cols = sorted(list(non_bg_cols))

    max_col = sorted_cols[-1] if sorted_cols else None
    col_R2 = sorted_cols[-2] if len(sorted_cols) > 1 else None

    return max_col, col_R2


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by projecting the two rightmost non-background
    pixels of each row onto two specific columns determined by the overall grid content.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Determine the background color
    background_color = find_background_color(input_np)

    # 2. & 3. Identify target columns max_col and col_R2
    max_col, col_R2 = find_target_columns(input_np, background_color)

    # Handle cases where target columns might not be found (e.g., grid is all background)
    if max_col is None:
        # If no non-background pixels, return the input grid (or an all-background grid)
        return input_np.tolist() # Or create a new background grid

    # 4. Create the output grid filled with background color
    output_np = np.full_like(input_np, background_color)

    # 5. Process each row
    for r in range(height):
        row = input_np[r, :]
        # 5a. Find non-background pixels and their column indices
        non_bg_indices = np.where(row != background_color)[0]

        # 5b. If non-background pixels exist in the row
        if non_bg_indices.size > 0:
            # Sort indices descending to easily get rightmost and second rightmost
            sorted_non_bg_indices = np.sort(non_bg_indices)[::-1]

            # i. Get the rightmost pixel's color and place it in the output at max_col
            rightmost_col_idx = sorted_non_bg_indices[0]
            rightmost_color = input_np[r, rightmost_col_idx]
            output_np[r, max_col] = rightmost_color

            # iii. If a second rightmost pixel exists and col_R2 is defined
            if len(sorted_non_bg_indices) > 1 and col_R2 is not None:
                second_rightmost_col_idx = sorted_non_bg_indices[1]
                second_rightmost_color = input_np[r, second_rightmost_col_idx]
                output_np[r, col_R2] = second_rightmost_color

    # 6. Return the result as a list of lists
    return output_np.tolist()