import numpy as np
from typing import List, Dict, Optional, Tuple

"""
Transforms an input grid based on identifying a pattern ('5'), a barrier ('6'), moving the pattern to the opposite side, drawing a diagonal trace from the original pattern's position, and marking the first barrier row with '9's based on the movement.

1.  Initialize a new grid (`output_grid`) with the same dimensions as the `input_grid`, filled entirely with the background color `1`.
2.  Identify the bounding box (`original_bounds`: min/max row/col) of the connected pattern of cells with color `5` in the `input_grid`. Also determine its width.
3.  Identify the starting row index (`barrier_row_idx`) of the solid block of rows containing only color `6` at the bottom of the `input_grid`.
4.  Copy all rows from `barrier_row_idx` to the bottom of the `input_grid` (the barrier) to the corresponding rows in `output_grid`.
5.  Determine the horizontal movement direction: if the `original_bounds['min_col']` is less than half the grid width, the pattern moves right; otherwise, it moves left.
6.  Calculate the bounding box (`moved_bounds`) for the pattern's destination in `output_grid`: maintain the original min/max rows; if moving right, set `min_col` to `grid_cols - width` and `max_col` to `grid_cols - 1`; if moving left, set `min_col` to `0` and `max_col` to `width - 1`.
7.  Copy the `5` colored cells from the `input_grid` within `original_bounds` to their corresponding relative positions within the `moved_bounds` in `output_grid`. Overwrite any existing values.
8.  Generate a diagonal trace:
    *   Set the diagonal step: `dr=1`. If moving right, `dc=1`; if moving left, `dc=-1`.
    *   For each cell `(r, c)` in the `input_grid` that is within `original_bounds` and has color `5`:
        *   Initialize the trace position `(cr, cc)` to `(r + dr, c + dc)`.
        *   While the trace position `(cr, cc)` is within the grid boundaries, is above the barrier (`cr < barrier_row_idx`), AND the cell `output_grid[cr, cc]` does *not* already contain color `5`:
            *   Set `output_grid[cr, cc]` to `5`.
            *   Update the trace position: `cr += dr`, `cc += dc`.
9.  Place the barrier markers:
    *   Calculate `start_col` and `end_col` (inclusive) for the markers based on movement direction and bounds.
    *   Overwrite the cells in `output_grid` at row `barrier_row_idx` from `start_col` to `end_col` (inclusive) with the marker color `9`.
"""


def find_pattern_bounds(grid: np.ndarray, value: int) -> Optional[Dict[str, int]]:
    """Finds the min/max row/col for all cells matching the given value."""
    rows_idx, cols_idx = np.where(grid == value)
    if rows_idx.size == 0:
        return None
    min_row = int(np.min(rows_idx))
    max_row = int(np.max(rows_idx))
    min_col = int(np.min(cols_idx))
    max_col = int(np.max(cols_idx))
    return {
        'min_row': min_row,
        'max_row': max_row,
        'min_col': min_col,
        'max_col': max_col,
        'width': max_col - min_col + 1,
        'height': max_row - min_row + 1
    }

def find_barrier_row(grid: np.ndarray, value: int) -> Optional[int]:
    """Finds the first row index consisting entirely of the barrier value."""
    rows, _ = grid.shape
    for r in range(rows):
        # Check if all elements in the row equal the barrier value
        # Using np.all is robust, but examples suggest barrier might just start
        # Let's find the first row CONTAINING the value, assuming structure
        if value in grid[r, :]:
            # Verify if it's the start of the barrier block
            is_barrier_start = True
            # Check if all rows from here down contain only 6 (or are out of bounds)
            # This is complex, let's simplify: Find first row with ANY 6s, assuming it's the start.
            rows_with_value, _ = np.where(grid == value)
            if rows_with_value.size > 0:
                return int(np.min(rows_with_value))
            else:
                return None # No barrier found
    return None # No barrier found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the transformation rules to the input grid."""
    
    # Convert input to numpy array for easier manipulation
    input_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape

    # 1. Initialize output grid with background value '1'
    output_arr = np.ones_like(input_arr) * 1

    # 2. Find the bounds of the '5' pattern
    original_bounds = find_pattern_bounds(input_arr, 5)
    if not original_bounds:
        # Handle case where pattern '5' is missing - return original or background?
        # Assuming pattern is always present based on examples. If not, copy barrier maybe.
        barrier_row_idx_fallback = find_barrier_row(input_arr, 6)
        if barrier_row_idx_fallback is not None:
            output_arr[barrier_row_idx_fallback:, :] = input_arr[barrier_row_idx_fallback:, :]
        return output_arr.tolist()

    # 3. Find the first row of the '6' barrier
    barrier_row_idx = find_barrier_row(input_arr, 6)
    if barrier_row_idx is None:
         # Handle case where barrier '6' is missing - assume it's off-grid?
         barrier_row_idx = rows # Treat as if barrier starts just after last row

    # 4. Copy the barrier from input to output
    if barrier_row_idx < rows:
        output_arr[barrier_row_idx:, :] = input_arr[barrier_row_idx:, :]

    # 5. Determine movement direction
    move_right = original_bounds['min_col'] < cols / 2
    pattern_width = original_bounds['width']
    pattern_height = original_bounds['height']

    # 6. Calculate moved bounds
    moved_bounds = {}
    moved_bounds['min_row'] = original_bounds['min_row']
    moved_bounds['max_row'] = original_bounds['max_row']
    if move_right:
        moved_bounds['min_col'] = cols - pattern_width
        moved_bounds['max_col'] = cols - 1
    else: # move_left
        moved_bounds['min_col'] = 0
        moved_bounds['max_col'] = pattern_width - 1

    # 7. Copy the moved pattern to the output grid
    # Iterate through the original pattern's bounding box
    for r_idx, r in enumerate(range(original_bounds['min_row'], original_bounds['max_row'] + 1)):
        for c_idx, c in enumerate(range(original_bounds['min_col'], original_bounds['max_col'] + 1)):
            # Check if the cell in the input actually contains the pattern value
            if input_arr[r, c] == 5:
                # Calculate the corresponding target cell in the moved position
                target_r = moved_bounds['min_row'] + r_idx
                target_c = moved_bounds['min_col'] + c_idx
                # Ensure target is within grid bounds before writing
                if 0 <= target_r < rows and 0 <= target_c < cols:
                     output_arr[target_r, target_c] = 5 # Overwrite whatever is there

    # 8. Generate the diagonal trace
    dr = 1
    dc = 1 if move_right else -1

    # Iterate through original pattern cells again
    for r in range(original_bounds['min_row'], original_bounds['max_row'] + 1):
        for c in range(original_bounds['min_col'], original_bounds['max_col'] + 1):
            # Start trace only from original '5' positions
            if input_arr[r, c] == 5:
                # Initialize trace start position (one step down diagonally)
                cr, cc = r + dr, c + dc
                # Loop while trace is valid
                while (0 <= cr < rows and          # within row bounds
                       0 <= cc < cols and          # within col bounds
                       cr < barrier_row_idx and    # above barrier
                       output_arr[cr, cc] != 5):   # does not collide with moved pattern
                    
                    # Place the trace '5'
                    output_arr[cr, cc] = 5
                    
                    # Move to the next diagonal position
                    cr += dr
                    cc += dc

    # 9. Place '9' markers in the first barrier row
    if barrier_row_idx < rows: # Check if barrier exists within grid
        start_9_col = 0
        end_9_col = 0 # Inclusive end column index

        if move_right:
            # Start at original pattern's left edge
            start_9_col = original_bounds['min_col']
            # End just past the moved pattern's left edge (derived from Ex2 metrics)
            end_9_col = moved_bounds['min_col'] + 1
            # Ex2: orig_min=0, moved_min=11. Target [0, 12]. start=0, end=11+1=12. Correct.
        else: # move_left
            # Start just past the moved pattern's right edge (derived from Ex1 metrics)
            start_9_col = moved_bounds['max_col'] + 1
            # End at the original pattern's right edge
            end_9_col = original_bounds['max_col']
            # Ex1: moved_max=4, orig_max=16. Target [5, 16]. start=4+1=5, end=16. Correct.

        # Clip column indices to be within grid bounds
        start_9_col = max(0, start_9_col)
        end_9_col = min(cols - 1, end_9_col) # Ensure end is valid index

        # Place markers if the range is valid
        if start_9_col <= end_9_col:
             output_arr[barrier_row_idx, start_9_col : end_9_col + 1] = 9 # Use end+1 for slicing

    # Convert back to list of lists for the final output
    return output_arr.tolist()