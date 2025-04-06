import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Transforms an input grid based on the following rules:

1.  Identify a connected pattern of '5's and a barrier of '6's at the bottom.
2.  Determine the bounding box of the '5' pattern.
3.  Create an output grid initialized with '1's (background).
4.  Move the '5' pattern horizontally to the opposite side of the grid, keeping its vertical position.
    - If the pattern starts on the left half, move it to the far right.
    - If the pattern starts on the right half, move it to the far left.
5.  Generate a diagonal 'trace' of '5's starting from the *original* position of each '5' in the pattern.
    - The trace goes down and right if the pattern moved right.
    - The trace goes down and left if the pattern moved left.
    - The trace stops if it hits the row just above the '6' barrier, goes out of bounds, or would overwrite the *moved* pattern.
6.  Identify the first row of the '6' barrier.
7.  Replace cells in this first barrier row with '9's. The horizontal span of the '9's depends on the original position and movement distance:
    - If moved right (started left): From the original pattern's start column to `original_start_col + movement_distance + 1`.
    - If moved left (started right): From `original_end_col - movement_distance + 1` to the original pattern's end column.
8.  Copy the remaining rows of the '6' barrier from the input to the output grid below the modified first barrier row.
"""

def find_pattern_bounds(grid: np.ndarray, value: int) -> Optional[Dict[str, int]]:
    """Finds the min/max row/col for all cells matching the given value."""
    rows, cols = np.where(grid == value)
    if rows.size == 0:
        return None
    return {
        'min_row': int(np.min(rows)),
        'max_row': int(np.max(rows)),
        'min_col': int(np.min(cols)),
        'max_col': int(np.max(cols)),
    }

def find_barrier_row(grid: np.ndarray, value: int) -> Optional[int]:
    """Finds the first row index consisting entirely of the barrier value."""
    rows, _ = grid.shape
    for r in range(rows):
        if np.all(grid[r, :] == value):
            return r
    # Fallback if no full row found, look for first row containing the value
    rows_with_value, _ = np.where(grid == value)
    if rows_with_value.size > 0:
        return int(np.min(rows_with_value))
    return None # Should not happen based on examples


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape

    # Initialize output grid with background value '1'
    output_arr = np.ones_like(input_arr) * 1

    # Find the bounds of the '5' pattern
    orig_bounds = find_pattern_bounds(input_arr, 5)
    if not orig_bounds:
        # If no pattern '5' found, return the initial grid or handle as needed
        # For now, assume '5' is always present based on examples
        # Copy the '6' barrier if it exists
        barrier_row_idx = find_barrier_row(input_arr, 6)
        if barrier_row_idx is not None:
             output_arr[barrier_row_idx:, :] = input_arr[barrier_row_idx:, :]
        return output_arr.tolist()


    # Find the first row of the '6' barrier
    barrier_row_idx = find_barrier_row(input_arr, 6)
    if barrier_row_idx is None:
         # Handle case where barrier '6' is missing - assume it's the bottom edge?
         # For now, assume '6' is always present
         barrier_row_idx = rows # Treat as if barrier is off-grid

    # --- Determine movement ---
    orig_width = orig_bounds['max_col'] - orig_bounds['min_col'] + 1
    orig_height = orig_bounds['max_row'] - orig_bounds['min_row'] + 1

    # Heuristic: If the pattern starts in the left half, move right, otherwise move left.
    move_right = orig_bounds['min_col'] < cols // 2
    moved_bounds = {}
    moved_bounds['min_row'] = orig_bounds['min_row']
    moved_bounds['max_row'] = orig_bounds['max_row']

    if move_right:
        moved_bounds['min_col'] = cols - orig_width
        moved_bounds['max_col'] = cols - 1
    else: # move_left
        moved_bounds['min_col'] = 0
        moved_bounds['max_col'] = orig_width - 1

    # --- Copy the moved pattern to the output grid ---
    for r_idx, r in enumerate(range(orig_bounds['min_row'], orig_bounds['max_row'] + 1)):
        for c_idx, c in enumerate(range(orig_bounds['min_col'], orig_bounds['max_col'] + 1)):
            if input_arr[r, c] == 5:
                target_r = moved_bounds['min_row'] + r_idx
                target_c = moved_bounds['min_col'] + c_idx
                if 0 <= target_r < rows and 0 <= target_c < cols:
                     output_arr[target_r, target_c] = 5

    # --- Generate the diagonal trace ---
    trace_dc = 1 if move_right else -1 # Direction of column change for trace

    for r in range(orig_bounds['min_row'], orig_bounds['max_row'] + 1):
        for c in range(orig_bounds['min_col'], orig_bounds['max_col'] + 1):
            # Start trace only from original '5' positions
            if input_arr[r, c] == 5:
                # Start trace one step down diagonally
                cr, cc = r + 1, c + trace_dc
                # Loop while trace is within bounds and above the barrier row
                while 0 <= cr < barrier_row_idx and 0 <= cc < cols:
                    # Check if the trace cell would overlap the moved pattern's bounding box
                    in_moved_box = (moved_bounds['min_row'] <= cr <= moved_bounds['max_row'] and
                                    moved_bounds['min_col'] <= cc <= moved_bounds['max_col'])
                    # Check if the specific cell in the moved area actually contains a 5
                    # This prevents stopping trace just because it enters the moved bounding box if that cell is background
                    # Important if the pattern isn't rectangular filled
                    overlaps_moved_pattern = False
                    if in_moved_box:
                         # Calculate corresponding original position to check if it was a 5
                         orig_r_check = cr - moved_bounds['min_row'] + orig_bounds['min_row']
                         orig_c_check = cc - moved_bounds['min_col'] + orig_bounds['min_col']
                         # Check if this calculated original position is valid and was a 5
                         if (orig_bounds['min_row'] <= orig_r_check <= orig_bounds['max_row'] and
                             orig_bounds['min_col'] <= orig_c_check <= orig_bounds['max_col'] and
                             input_arr[orig_r_check, orig_c_check] == 5):
                               overlaps_moved_pattern = True


                    if overlaps_moved_pattern:
                        break # Stop trace if it hits the actual moved pattern

                    # Place the trace '5'
                    output_arr[cr, cc] = 5

                    # Move to the next diagonal position
                    cr += 1
                    cc += trace_dc

    # --- Generate '9' markers in the first barrier row ---
    if barrier_row_idx < rows: # Check if barrier exists within grid
        move_dist = abs(moved_bounds['min_col'] - orig_bounds['min_col'])
        start_9_col = 0
        end_9_col = 0 # Exclusive end for slicing/range

        if move_right:
            start_9_col = orig_bounds['min_col']
            # End column needs careful check - it should go up to where the trace ends or movement ends
            # Using the formula derived in thought: orig_min_col + move_dist + 1
            end_9_col = orig_bounds['min_col'] + move_dist + 1 # Exclusive index
            # Example 2: start=0, end=0+11+1=12. Fill cols 0..11 -> No, output shows 0..12 filled.
            # Let's try end = start + move_dist + pattern_width ? No..
            # Let's stick to the derived formula end = start + move_dist + 1. This makes range [start, start+move_dist].
            # Example 2: start=0, move_dist=11 -> range [0, 11]. Output has 0..12. Off by one.
            # Maybe end_9_col = moved_bounds['max_col'] - orig_width + 1 + move_dist + 1? No..
            # Revisit calculation: start = 0. end = 0 + 11 = 11. If range is inclusive [start, end+1]? [0, 12]. Yes.
            end_9_col = orig_bounds['min_col'] + move_dist + 1 # Let's try making this inclusive end, so slice needs +1

        else: # move_left
            start_9_col = orig_bounds['max_col'] - move_dist + 1
            # Example 1: start = 16 - 12 + 1 = 5.
            end_9_col = orig_bounds['max_col'] # Inclusive end
            # Example 1: range [5, 16]. Correct.

        # Ensure columns are within grid bounds before slicing
        start_9_col = max(0, start_9_col)
        end_9_col = min(cols, end_9_col + 1) # Add 1 for exclusive slicing index

        if start_9_col < end_9_col: # Check if range is valid
            output_arr[barrier_row_idx, start_9_col:end_9_col] = 9

    # --- Copy the rest of the '6' barrier ---
    if barrier_row_idx is not None and barrier_row_idx + 1 < rows:
        output_arr[barrier_row_idx + 1:, :] = input_arr[barrier_row_idx + 1:, :]

    # Convert back to list of lists for the final output
    return output_arr.tolist()
