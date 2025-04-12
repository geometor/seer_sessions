```python
"""
Transforms an input grid by rearranging its single non-background color pixels into a specific shape in the bottom-left corner. This shape is derived from a right-angled triangle T(H).

1.  Analyze Input: Find the non-background color 'C' and its count 'N'. Get grid dimensions (H_grid, W_grid).
2.  Determine Target Triangle Size: Find the smallest integer H such that the triangular number T(H) = H*(H+1)/2 is greater than or equal to N.
3.  Generate Base Triangle Pixels: Create a list P of coordinates (r, c) for the full triangle T(H) defined by: r >= H_grid - H, c <= H - 1, and r + c >= H_grid - 1.
4.  Identify Pixels to Remove: Calculate R = T(H) - N. If R > 0, find the R pixels in P that are not in the bottom row (r < H_grid - 1) and not in the rightmost column of the triangle's bounding box (c < H - 1). Sort these candidates by column (ascending) then row (ascending), and select the first R as the pixels to remove (P_remove).
5.  Construct Output Grid: Create an output grid. Iterate through the base triangle pixels P. If a pixel is not in P_remove, paint it with color C.
6.  Finalize: Return the generated grid.
"""

import numpy as np
import math

def calculate_triangle_number(h: int) -> int:
    """Calculates the h-th triangular number."""
    if h < 0:
        return 0
    return h * (h + 1) // 2

def find_smallest_h(n: int) -> int:
    """Finds the smallest integer H such that T(H) >= n."""
    if n <= 0:
        return 0
    h = 0
    while calculate_triangle_number(h) < n:
        h += 1
    return h

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    H_grid, W_grid = input_np.shape
    background_color = 0

    # 1. Analyze Input
    non_bg_coords = np.argwhere(input_np != background_color)
    count_N = len(non_bg_coords)

    # Handle edge case: empty input grid
    if count_N == 0:
        return np.zeros_like(input_np).tolist()

    # Get the single non-background color
    color_C = input_np[non_bg_coords[0][0], non_bg_coords[0][1]]

    # 2. Determine Target Triangle Size
    H = find_smallest_h(count_N)
    T_H = calculate_triangle_number(H)

    # 3. Generate Base Triangle Pixels
    base_triangle_pixels_P = []
    for r in range(H_grid):
        for c in range(W_grid):
            # Conditions for belonging to triangle T(H) in bottom-left
            if r >= H_grid - H and c <= H - 1 and r + c >= H_grid - 1:
                base_triangle_pixels_P.append((r, c))

    # 4. Identify Pixels to Remove (if N is not triangular)
    pixels_to_remove_R = T_H - count_N
    P_remove = []

    if pixels_to_remove_R > 0:
        # Filter candidates for removal: not in bottom row AND not in rightmost column
        P_candidates_for_removal = []
        for r, c in base_triangle_pixels_P:
            is_not_bottom_row = (r < H_grid - 1)
            is_not_rightmost_col = (c < H - 1) # Check against triangle dim H, not grid dim W_grid
            if is_not_bottom_row and is_not_rightmost_col:
                 P_candidates_for_removal.append((r, c))

        # Sort candidates: primarily by column (asc), secondarily by row (asc)
        P_candidates_for_removal.sort(key=lambda coord: (coord[1], coord[0]))

        # Select the first R candidates to remove
        P_remove = P_candidates_for_removal[:pixels_to_remove_R]

    # 5. Construct Output Grid
    output_np = np.full_like(input_np, background_color)
    P_remove_set = set(P_remove) # Convert to set for faster lookup

    # Iterate through the base triangle pixels and paint if not marked for removal
    for r, c in base_triangle_pixels_P:
        if (r, c) not in P_remove_set:
            output_np[r, c] = color_C

    # 6. Finalize
    return output_np.tolist()
```