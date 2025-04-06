```python
"""
Transforms an input grid based on the following logic:
1. Identifies four corner values from the absolute corners of the input grid (Top-Left, Top-Right, Bottom-Left, Bottom-Right).
2. Locates a rectangular frame composed of '1's within the input grid.
3. Extracts the subgrid (internal pattern) located strictly inside the '1' frame, which consists of '0's and '8's.
4. Creates an output grid with the same dimensions as the internal pattern grid.
5. Populates the output grid by iterating through the internal pattern:
   - If a cell in the internal pattern is '0', the corresponding cell in the output grid is set to '0'.
   - If a cell in the internal pattern is '8', the corresponding cell in the output grid is set to one of the corner values based on the cell's quadrant within the internal pattern (TL quadrant maps to TL corner value, TR to TR, BL to BL, BR to BR).
"""

import numpy as np
from typing import List, Tuple

def find_frame_boundaries(grid: np.ndarray) -> Tuple[int, int, int, int]:
    """Finds the row and column indices defining the inner boundary of the '1' frame."""
    rows, cols = grid.shape
    min_row, max_row = -1, -1
    min_col, max_col = -1, -1

    # Find first and last rows containing non-1s (to identify frame roughly)
    # This assumes the frame isn't at the absolute edge, which holds for examples
    for r in range(rows):
        if not np.all(grid[r] == 1):
            if min_row == -1:
                min_row = r
            max_row = r

    for c in range(cols):
         if not np.all(grid[:, c] == 1):
            if min_col == -1:
                min_col = c
            max_col = c

    # The internal pattern is *inside* the frame, so boundaries are +1/-1
    # Note: This logic assumes a frame of thickness 1 surrounding the internal pattern.
    # Based on examples, the frame seems to be exactly at row/col `min_row`, `max_row`, `min_col`, `max_col`.
    # So the internal pattern starts at row `min_row + 1` and col `min_col + 1`.
    frame_top = min_row
    frame_bottom = max_row
    frame_left = min_col
    frame_right = max_col

    # The internal pattern is between these frame boundaries
    internal_top = frame_top + 1
    internal_bottom = frame_bottom -1 # Exclusive index for slicing
    internal_left = frame_left + 1
    internal_right = max_col - 1 # Exclusive index for slicing

    # Return the start/end indices for slicing the internal pattern
    return internal_top, internal_bottom + 1, internal_left, internal_right + 1


def extract_internal_pattern(grid: np.ndarray, top: int, bottom: int, left: int, right: int) -> np.ndarray:
    """Extracts the subgrid within the given boundaries."""
    return grid[top:bottom, left:right]

def get_corner_values(grid: np.ndarray) -> Tuple[int, int, int, int]:
    """Extracts the four corner values from the absolute corners of the grid."""
    rows, cols = grid.shape
    tl = grid[0, 0]
    tr = grid[0, cols - 1]
    bl = grid[rows - 1, 0]
    br = grid[rows - 1, cols - 1]
    return tl, tr, bl, br

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)

    # --- Identify Components ---
    # 1. Get the four corner values
    tl_corner, tr_corner, bl_corner, br_corner = get_corner_values(grid_np)

    # 2. Find the boundaries of the internal pattern (inside the '1' frame)
    # We need to locate the frame first. Frame rows/cols usually contain only '1's
    # except where they intersect the internal pattern area.
    # A simpler approach for the given examples: find the first/last row/col
    # that is *not* entirely composed of '1's. The internal pattern is inside this.
    
    rows_with_non_ones = [r for r in range(grid_np.shape[0]) if not np.all(grid_np[r] == 1)]
    cols_with_non_ones = [c for c in range(grid_np.shape[1]) if not np.all(grid_np[:, c] == 1)]
    
    if not rows_with_non_ones or not cols_with_non_ones:
         # Handle cases where no clear frame/internal pattern is found (e.g., all 1s)
         # Based on examples, this shouldn't happen.
         # Let's assume frame exists and find its boundaries more directly
         # Find rows/cols that contain a '1' but are not *all* '1's - these define the frame boundary adjacent to the pattern
         
         frame_rows = []
         for r in range(grid_np.shape[0]):
             row = grid_np[r,:]
             if 1 in row and not np.all(row == 1):
                 frame_rows.append(r)
         frame_cols = []
         for c in range(grid_np.shape[1]):
              col = grid_np[:,c]
              if 1 in col and not np.all(col == 1):
                  frame_cols.append(c)
         
         if not frame_rows or not frame_cols:
            # Fallback or raise error if frame isn't found
            # Based on structure, the core pattern should be bounded by 1s
            # Let's try the boundary finding function
             try:
                 internal_top, internal_bottom, internal_left, internal_right = find_frame_boundaries(grid_np)
             except: # If boundary finding fails, maybe it's a simpler case?
                 raise ValueError("Could not determine frame boundaries.") # Or return empty?
         else:
             internal_top = min(frame_rows) + 1
             internal_bottom = max(frame_rows) # Exclusive index for slicing
             internal_left = min(frame_cols) + 1
             internal_right = max(frame_cols) # Exclusive index for slicing

    else:
        # The internal pattern rows/cols are between the min/max row/col containing non-1s
        internal_top = min(rows_with_non_ones)
        internal_bottom = max(rows_with_non_ones) + 1 # Exclusive index for slicing
        internal_left = min(cols_with_non_ones)
        internal_right = max(cols_with_non_ones) + 1 # Exclusive index for slicing


    # 3. Extract the internal pattern subgrid
    internal_pattern = grid_np[internal_top:internal_bottom, internal_left:internal_right]

    # --- Initialize Output ---
    # Get dimensions of the internal pattern
    h, w = internal_pattern.shape
    # Create output grid with the same dimensions, initialized perhaps with zeros
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
                # Determine quadrant (using floating point division for midpoint)
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
            # Handle unexpected values if necessary (though examples only show 0 and 8)
            # else:
            #    output_grid_np[r, c] = v # or some error value?

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    # --- Return Output ---
    return output_grid
```