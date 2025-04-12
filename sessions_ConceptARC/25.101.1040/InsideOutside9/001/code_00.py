import numpy as np
import copy

"""
Identifies two parallel red lines (either horizontal or vertical) which act as barriers. 
Filters out yellow pixels, keeping only those located strictly between the red lines. 
If the lines are vertical, the filtering is based on column index; if horizontal, 
it's based on row index. All other pixels (red barriers and white background) remain unchanged.
"""

def find_pixel_coordinates(grid: np.ndarray, value: int) -> list[tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific value."""
    rows, cols = np.where(grid == value)
    return list(zip(rows, cols))

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Filters yellow pixels based on their position relative to red barrier lines.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # 1. Identify the coordinates of all red (2) pixels (barriers).
    red_coords = find_pixel_coordinates(input_np, 2)

    # If no red barriers are present, maybe return the input unchanged or handle differently?
    # Based on examples, barriers exist. Assuming they always do for the core logic.
    if not red_coords:
        # Or perhaps clear all yellow pixels if no boundary is defined?
        # Let's clear yellow if no barriers, matching train_2 implicit behavior
        # where yellow pixels outside bounds are cleared.
        yellow_coords = find_pixel_coordinates(input_np, 4)
        for r, c in yellow_coords:
            output_np[r, c] = 0
        return output_np.tolist()


    # 2. Determine the orientation of the barriers:
    red_rows = {r for r, c in red_coords}
    red_cols = {c for r, c in red_coords}
    num_rows = len(red_rows)
    num_cols = len(red_cols)

    min_coord = -1
    max_coord = -1
    is_horizontal = False

    # a. If num_rows < num_cols, the barriers are horizontal.
    # Handles cases with potentially more than 2 lines, but uses min/max extent.
    if num_rows > 0 and num_cols > 0 : # Check if red pixels exist
        if num_rows < num_cols :
             is_horizontal = True
             min_coord = min(red_rows)
             max_coord = max(red_rows)
        # b. Otherwise (assume num_cols <= num_rows), the barriers are vertical.
        else:
             is_horizontal = False
             min_coord = min(red_cols)
             max_coord = max(red_cols)
    
    # 3. Find yellow pixel coordinates
    yellow_coords = find_pixel_coordinates(input_np, 4)

    # 4. Iterate through each yellow pixel (r, c) and apply filtering.
    for r, c in yellow_coords:
        keep_pixel = False
        # a. If barriers are horizontal: Check row condition
        if is_horizontal:
            if min_coord < r < max_coord:
                keep_pixel = True
        # b. If barriers are vertical: Check column condition
        else: # Vertical
            if min_coord < c < max_coord:
                keep_pixel = True

        # If the condition to keep is *not* met, change the pixel to white (0).
        if not keep_pixel:
            output_np[r, c] = 0

    # 5. Convert back to list of lists and return.
    return output_np.tolist()