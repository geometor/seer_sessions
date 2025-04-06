"""
Transforms an input grid based on the following logic:
1. Identifies four corner values from the absolute corners of the input grid (Top-Left, Top-Right, Bottom-Left, Bottom-Right).
2. Locates a rectangular frame composed entirely of '1's within the input grid.
3. Extracts the subgrid (internal pattern) located strictly inside this '1' frame. This internal pattern consists of '0's and '8's.
4. Creates an output grid with the same dimensions as the extracted internal pattern grid.
5. Populates the output grid by iterating through the internal pattern:
   - If a cell in the internal pattern is '0', the corresponding cell in the output grid is set to '0'.
   - If a cell in the internal pattern is '8', the corresponding cell in the output grid is set to one of the input's corner values based on the cell's quadrant within the internal pattern (TL quadrant maps to input's TL corner value, TR to TR, BL to BL, BR to BR).
"""

import numpy as np
from typing import List, Tuple

def get_corner_values(grid: np.ndarray) -> Tuple[int, int, int, int]:
    """Extracts the four corner values from the absolute corners of the grid."""
    rows, cols = grid.shape
    tl = grid[0, 0]
    tr = grid[0, cols - 1]
    bl = grid[rows - 1, 0]
    br = grid[rows - 1, cols - 1]
    return tl, tr, bl, br

def find_internal_pattern_bounds(grid: np.ndarray) -> Tuple[int, int, int, int]:
    """
    Finds the row and column indices for slicing the internal pattern.
    It assumes the internal pattern is bounded by rows and columns consisting entirely of '1's.
    Returns (top_row, bottom_row_exclusive, left_col, right_col_exclusive).
    """
    rows, cols = grid.shape
    
    # Find indices of rows composed entirely of '1's
    all_one_rows = [r for r in range(rows) if np.all(grid[r, :] == 1)]
    if not all_one_rows or len(all_one_rows) < 2:
        raise ValueError("Could not find bounding rows of '1's for the frame.")
        
    # Find indices of columns composed entirely of '1's
    all_one_cols = [c for c in range(cols) if np.all(grid[:, c] == 1)]
    if not all_one_cols or len(all_one_cols) < 2:
         raise ValueError("Could not find bounding columns of '1's for the frame.")

    # Internal pattern is between the first and last all-'1' row/column
    internal_top = min(all_one_rows) + 1
    internal_bottom = max(all_one_rows) # Exclusive index for slicing
    internal_left = min(all_one_cols) + 1
    internal_right = max(all_one_cols) # Exclusive index for slicing

    # Basic validation: ensure bounds are sensible
    if not (0 <= internal_top < internal_bottom <= rows and 0 <= internal_left < internal_right <= cols):
         raise ValueError(f"Calculated invalid bounds: {internal_top, internal_bottom, internal_left, internal_right}")
         
    return internal_top, internal_bottom, internal_left, internal_right

def extract_internal_pattern(grid: np.ndarray, bounds: Tuple[int, int, int, int]) -> np.ndarray:
    """Extracts the subgrid within the given boundaries."""
    top, bottom, left, right = bounds
    return grid[top:bottom, left:right]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)

    # --- Identify Components ---
    # 1. Get the four corner values from the input grid
    tl_corner, tr_corner, bl_corner, br_corner = get_corner_values(grid_np)

    # 2. Find the boundaries of the internal pattern (inside the '1' frame)
    try:
        bounds = find_internal_pattern_bounds(grid_np)
    except ValueError as e:
        print(f"Error finding bounds: {e}")
        # Handle error case: perhaps return empty grid or re-raise
        # For this problem structure, an error likely indicates an unexpected input format.
        return [] 

    # 3. Extract the internal pattern subgrid
    internal_pattern = extract_internal_pattern(grid_np, bounds)

    # --- Initialize Output ---
    # Get dimensions of the internal pattern
    h, w = internal_pattern.shape
    if h == 0 or w == 0:
        # Handle empty internal pattern case if necessary
        return []
        
    # Create output grid with the same dimensions as the internal pattern
    output_grid_np = np.zeros((h, w), dtype=int)

    # --- Populate Output Grid ---
    # Iterate through each cell (r, c) of the internal pattern
    for r in range(h):
        for c in range(w):
            # Get the value 'v' from the internal pattern
            v = internal_pattern[r, c]

            # If v is 0, copy 0 to the output
            if v == 0:
                output_grid_np[r, c] = 0
            # If v is 8, determine the quadrant and assign the corresponding corner value
            elif v == 8:
                # Determine quadrant using floating point division for midpoint comparison
                # Top-Left quadrant
                if r < h / 2 and c < w / 2:
                    output_grid_np[r, c] = tl_corner
                # Top-Right quadrant
                elif r < h / 2 and c >= w / 2:
                    output_grid_np[r, c] = tr_corner
                # Bottom-Left quadrant
                elif r >= h / 2 and c < w / 2:
                    output_grid_np[r, c] = bl_corner
                # Bottom-Right quadrant
                elif r >= h / 2 and c >= w / 2:
                    output_grid_np[r, c] = br_corner
            # else: # Optional: handle unexpected values in internal pattern
            #    output_grid_np[r, c] = v # or raise error, or assign default

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    # --- Return Output ---
    return output_grid