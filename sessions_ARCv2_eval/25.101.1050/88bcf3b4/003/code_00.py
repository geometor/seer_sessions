import numpy as np
from collections import Counter
import math

"""
The transformation operates on two specific columns determined by the input grid's content: 
C1 (the rightmost column with any non-background pixel) and C2 (the second rightmost column with any non-background pixel).
It identifies the topmost non-background pixel in each of these input columns (V_top_C1 at R_top_C1, and V_top_C2 at R_top_C2).
The output grid is initialized with the background color.
Then, column C1 of the output is populated: pixels from input column C1 are copied if they are not background; background pixels in output C1 *above* R_top_C1 are filled with V_top_C2.
Next, column C2 of the output is populated: pixels from input column C2 are copied if they are not background; background pixels in output C2 *above* R_top_C2 are filled with V_top_C2, but *only if* a condition based on the content of column C1 at the same row is met (specifically, if the already computed output value at C1 is background, OR if the original input value at C1 was V_top_C1).
All other columns in the output remain background color.
"""

def find_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid, assumed to be the background."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default background if grid is empty
    # Simplification: Assume most frequent color is background
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_target_columns(grid: np.ndarray, background_color: int) -> tuple[int | None, int | None]:
    """
    Finds the indices of the rightmost (C1) and second rightmost (C2) columns
    containing non-background pixels.
    Returns (C1, C2). Returns None for an index if not found.
    """
    rows, cols = grid.shape
    non_bg_cols = set()
    for c in range(cols):
        if np.any(grid[:, c] != background_color):
            non_bg_cols.add(c)

    sorted_cols = sorted(list(non_bg_cols))

    C1 = sorted_cols[-1] if sorted_cols else None
    C2 = sorted_cols[-2] if len(sorted_cols) > 1 else None

    return C1, C2

def find_topmost_non_background(grid: np.ndarray, col_idx: int, background_color: int, height: int) -> tuple[int, int]:
    """
    Finds the row index (R_top) and value (V_top) of the topmost
    non-background pixel in the specified column.
    Returns (R_top, V_top). If column is empty or invalid,
    returns (height, background_color).
    """
    if col_idx is None or col_idx < 0 or col_idx >= grid.shape[1]:
        return height, background_color # Indicate no pixel found

    column_data = grid[:, col_idx]
    non_bg_indices = np.where(column_data != background_color)[0]

    if non_bg_indices.size == 0:
        return height, background_color # Indicate no pixel found

    R_top = non_bg_indices[0]
    V_top = grid[R_top, col_idx]
    return R_top, V_top


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the defined logic involving C1, C2,
    and upward filling based on topmost pixels V_top_C1 and V_top_C2.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Determine the background color
    bg = find_background_color(input_np)

    # 2. & 3. Identify target columns C1 and C2
    C1, C2 = find_target_columns(input_np, bg)

    # Handle edge case: No non-background pixels found
    if C1 is None:
        return input_grid # Or return np.full_like(input_np, bg).tolist()

    # 4. Find topmost non-background pixel in C1
    R_top_C1, V_top_C1 = find_topmost_non_background(input_np, C1, bg, height)

    # 5. Find topmost non-background pixel in C2
    # Note: If C2 is None, find_topmost_non_background handles it correctly
    R_top_C2, V_top_C2 = find_topmost_non_background(input_np, C2, bg, height)

    # 6. Create the output grid filled with background color
    output_np = np.full_like(input_np, bg)

    # 7. Process output column C1
    for r in range(height):
        V_current_C1 = input_np[r, C1]
        if V_current_C1 != bg:
            # 7b. Copy non-background pixel from input C1
            output_np[r, C1] = V_current_C1
        elif r < R_top_C1:
             # 7c. Fill background cells above R_top_C1 with V_top_C2
            output_np[r, C1] = V_top_C2
        # else: leave as background (already initialized)

    # 8. Process output column C2 (only if C2 exists)
    if C2 is not None:
        for r in range(height):
            V_current_C2 = input_np[r, C2]
            if V_current_C2 != bg:
                # 8b. Copy non-background pixel from input C2
                output_np[r, C2] = V_current_C2
            elif r < R_top_C2:
                # 8c. Check condition for upward fill
                # Condition: (output[r, C1] == bg) OR (input[r, C1] == V_top_C1)
                # Note: Need to handle the case where V_top_C1 might be bg if C1 was empty,
                # but find_topmost_non_background ensures V_top_C1 is bg only if R_top_C1 is height.
                # The input[r, C1] == V_top_C1 check only makes sense if V_top_C1 is not bg.
                condition_met = False
                if output_np[r, C1] == bg:
                    condition_met = True
                # Check second part of OR only if V_top_C1 was actually found
                elif R_top_C1 < height and input_np[r, C1] == V_top_C1:
                     condition_met = True

                if condition_met:
                     # Fill background cells above R_top_C2 with V_top_C2 if condition met
                    output_np[r, C2] = V_top_C2
            # else: leave as background (already initialized)

    # 9. Return the result as a list of lists
    return output_np.tolist()