import numpy as np
from typing import List, Tuple

"""
The transformation identifies three key adjacent rows in the input grid based on a specific pattern in the middle row.
1. Find the "center row": Locate a row containing a horizontal sequence of three non-white pixels where the outer two pixels have the same color (X) and the middle pixel has a different color (Y), forming an "X Y X" pattern.
2. Identify "upper row" and "lower row": These are the rows directly above and below the center row, respectively.
3. Initialize the output grid as a copy of the input grid.
4. Apply transformations based on these three rows:
    a. Center Row (Horizontal Expansion): Extend the color X from the "X Y X" pattern horizontally outwards to fill the rest of the center row in the output grid, leaving the original "X Y X" pixels unchanged.
    b. Upper Row (Upward Projection): For each non-white pixel in the upper row of the input grid:
        - Find the horizontal segment of non-white pixels it belongs to.
        - Calculate the center column of this segment.
        - Calculate the pixel's horizontal offset from the segment center.
        - Project the pixel one step upwards and horizontally by its offset. Place the pixel's color at this new location in the output grid.
    c. Lower Row (Downward Projection & Ray Casting): For each non-white pixel in the lower row of the input grid:
        - Find the horizontal segment of non-white pixels it belongs to.
        - Calculate the center column of this segment.
        - Calculate the pixel's horizontal offset from the segment center.
        - Project the pixel one step downwards and horizontally by its offset. Place the pixel's color at this new location in the output grid.
        - Cast a "ray" of the same color downwards from this projected position. The ray goes straight down if the offset was zero, diagonally down-left if the offset was negative, and diagonally down-right if the offset was positive. The ray continues until it hits the grid boundary.
5. Return the modified output grid.
"""

def find_center_row(grid: np.ndarray) -> Tuple[int, int, int, int, int]:
    """
    Finds the row index and column indices of the 'X Y X' pattern.
    Returns (row_idx, x_color, left_x_col, y_col, right_x_col) or raises ValueError if not found.
    """
    height, width = grid.shape
    for r in range(height):
        for c in range(width - 2):
            p1, p2, p3 = grid[r, c], grid[r, c + 1], grid[r, c + 2]
            # Check for X Y X pattern (non-white)
            if p1 != 0 and p2 != 0 and p3 != 0 and p1 == p3 and p1 != p2:
                # Check if the pattern is isolated horizontally by white pixels or grid edges
                left_ok = (c == 0 or grid[r, c - 1] == 0)
                right_ok = (c + 3 == width or grid[r, c + 3] == 0)
                if left_ok and right_ok:
                     return r, p1, c, c + 1, c + 2
    raise ValueError("Center 'X Y X' pattern not found")

def find_horizontal_segment(grid: np.ndarray, r: int, c: int) -> Tuple[int, int]:
    """Finds the start and end column index of a horizontal segment of non-white pixels."""
    if r < 0 or r >= grid.shape[0] or grid[r, c] == 0:
        raise ValueError(f"Pixel at ({r}, {c}) is white or out of bounds")

    width = grid.shape[1]
    start_col = c
    while start_col > 0 and grid[r, start_col - 1] != 0:
        start_col -= 1

    end_col = c
    while end_col < width - 1 and grid[r, end_col + 1] != 0:
        end_col += 1

    return start_col, end_col

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the described transformation to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    try:
        # 1. Find the center row and the 'X Y X' pattern
        center_row_idx, x_color, left_x_col, y_col, right_x_col = find_center_row(input_np)
        upper_row_idx = center_row_idx - 1
        lower_row_idx = center_row_idx + 1

        # 4a. Center Row Horizontal Expansion
        # Fill left side
        for c in range(left_x_col):
            output_np[center_row_idx, c] = x_color
        # Fill right side
        for c in range(right_x_col + 1, width):
            output_np[center_row_idx, c] = x_color
        # Ensure original X Y X is preserved (already copied, but good practice)
        # output_np[center_row_idx, left_x_col:right_x_col+1] = input_np[center_row_idx, left_x_col:right_x_col+1]

        # 4b. Upper Row Upward Projection
        if upper_row_idx >= 0:
            processed_cols_upper = set()
            for c_orig in range(width):
                if c_orig in processed_cols_upper:
                    continue
                if input_np[upper_row_idx, c_orig] != 0:
                    color = input_np[upper_row_idx, c_orig]
                    start_col, end_col = find_horizontal_segment(input_np, upper_row_idx, c_orig)
                    mid_col = start_col + (end_col - start_col) // 2

                    # Process all pixels in this segment
                    for c_seg in range(start_col, end_col + 1):
                         if input_np[upper_row_idx, c_seg] != 0: # Check again as segments might merge oddly
                            seg_color = input_np[upper_row_idx, c_seg]
                            offset = c_seg - mid_col
                            target_row = upper_row_idx - 1
                            target_col = c_seg + offset # Project horizontally by offset

                            if 0 <= target_row < height and 0 <= target_col < width:
                                output_np[target_row, target_col] = seg_color
                            processed_cols_upper.add(c_seg)


        # 4c. Lower Row Downward Projection & Ray Casting
        if lower_row_idx < height:
            processed_cols_lower = set()
            for c_orig in range(width):
                 if c_orig in processed_cols_lower:
                     continue
                 if input_np[lower_row_idx, c_orig] != 0:
                    color = input_np[lower_row_idx, c_orig]
                    start_col, end_col = find_horizontal_segment(input_np, lower_row_idx, c_orig)
                    mid_col = start_col + (end_col - start_col) // 2

                    # Process all pixels in this segment
                    for c_seg in range(start_col, end_col + 1):
                        if input_np[lower_row_idx, c_seg] != 0: # Check again
                            seg_color = input_np[lower_row_idx, c_seg]
                            offset = c_seg - mid_col
                            
                            # --- Single Step Projection ---
                            target_row = lower_row_idx + 1
                            target_col = c_seg + offset # Project horizontally by offset

                            proj_r, proj_c = -1, -1 # Store projection coords for ray start
                            if 0 <= target_row < height and 0 <= target_col < width:
                                output_np[target_row, target_col] = seg_color
                                proj_r, proj_c = target_row, target_col

                            # --- Ray Casting ---
                            if proj_r != -1: # Only cast if initial projection was in bounds
                                dr, dc = 1, 0  # Default: straight down
                                if offset < 0:
                                    dc = -1  # Diagonal down-left
                                elif offset > 0:
                                    dc = 1  # Diagonal down-right

                                # Start ray from the *next* position after the single step projection
                                ray_r, ray_c = proj_r + dr, proj_c + dc
                                while 0 <= ray_r < height and 0 <= ray_c < width:
                                    output_np[ray_r, ray_c] = seg_color
                                    ray_r += dr
                                    ray_c += dc
                            processed_cols_lower.add(c_seg)


    except ValueError as e:
        # If the characteristic pattern isn't found, return the input unchanged
        # Or handle the error as appropriate for the specific ARC task context
        # For now, returning a copy is safer.
        print(f"Warning: {e}. Returning copy of input.")
        return input_np.tolist()


    return output_np.tolist()