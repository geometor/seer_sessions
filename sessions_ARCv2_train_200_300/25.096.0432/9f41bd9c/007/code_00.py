import numpy as np
from typing import List, Dict, Optional, Tuple, Set

"""
Transforms an input grid based on the following sequential steps:
1.  Initializes an output grid filled with background color '1'.
2.  Identifies the '5' pattern (coordinates and bounds) and the first '6' barrier row in the input.
3.  Copies the barrier rows (starting from the identified barrier row) from the input to the output.
4.  Generates diagonal traces ('5') extending from each original '5' position, stopping at grid boundaries or the barrier row. These traces are drawn onto the output grid.
5.  Moves the original '5' pattern to the opposite horizontal side of the grid, drawing it onto the output grid and overwriting any trace cells in the destination area.
6.  Places '9' markers on the first barrier row in the output grid, based on the original and moved positions of the pattern, overwriting the initially copied '6's.
"""

def find_pattern_coords_and_bounds(grid: np.ndarray, value: int) -> Tuple[Optional[Set[Tuple[int, int]]], Optional[Dict[str, int]]]:
    """Finds all coordinates and the bounding box for cells matching the given value."""
    rows_idx, cols_idx = np.where(grid == value)
    if rows_idx.size == 0:
        return None, None
        
    coords = set(zip(rows_idx.tolist(), cols_idx.tolist()))
    
    min_row = int(np.min(rows_idx))
    max_row = int(np.max(rows_idx))
    min_col = int(np.min(cols_idx))
    max_col = int(np.max(cols_idx))
    
    bounds = {
        'min_row': min_row,
        'max_row': max_row,
        'min_col': min_col,
        'max_col': max_col,
        'width': max_col - min_col + 1,
        'height': max_row - min_row + 1
    }
    return coords, bounds

def find_barrier_row(grid: np.ndarray, value: int) -> Optional[int]:
    """Finds the first row index containing the barrier value."""
    rows, _ = grid.shape
    rows_with_value, _ = np.where(grid == value)
    if rows_with_value.size > 0:
        return int(np.min(rows_with_value))
    return None # No barrier found

def calculate_moved_bounds(original_bounds: Dict[str, int], grid_cols: int, move_right: bool) -> Dict[str, int]:
    """Calculates the bounding box for the pattern's destination."""
    moved_bounds = {}
    moved_bounds['min_row'] = original_bounds['min_row']
    moved_bounds['max_row'] = original_bounds['max_row']
    pattern_width = original_bounds['width']
    
    if move_right:
        moved_bounds['min_col'] = grid_cols - pattern_width
        moved_bounds['max_col'] = grid_cols - 1
    else: # move_left
        moved_bounds['min_col'] = 0
        moved_bounds['max_col'] = pattern_width - 1
    moved_bounds['width'] = pattern_width
    moved_bounds['height'] = original_bounds['height']
    
    return moved_bounds

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the transformation rules to the input grid."""
    
    # Convert input to numpy array for easier manipulation
    input_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape

    # 1. Initialize output grid with background value '1'
    output_arr = np.ones_like(input_arr) * 1

    # 2. Identify pattern ('5') and barrier ('6')
    original_coords, original_bounds = find_pattern_coords_and_bounds(input_arr, 5)
    barrier_row_idx = find_barrier_row(input_arr, 6)
    
    # If no barrier found, treat it as being just off the bottom of the grid
    if barrier_row_idx is None:
         barrier_row_idx = rows 

    # 3. Copy barrier rows from input to output
    if barrier_row_idx < rows:
        output_arr[barrier_row_idx:, :] = input_arr[barrier_row_idx:, :]

    # If no pattern found, return the grid with only the barrier copied
    if not original_coords or not original_bounds:
        return output_arr.tolist()

    # --- Pattern exists, proceed with transformation ---

    # 5. Determine movement direction and trace steps
    move_right = original_bounds['min_col'] < cols / 2.0
    dr = 1
    dc = 1 if move_right else -1

    # 6. Generate Traces (draw first)
    for r_orig, c_orig in original_coords:
        k = 1
        while True:
            # Calculate next trace point
            nr, nc = r_orig + k * dr, c_orig + k * dc

            # Check termination conditions: Out of bounds or hit barrier row
            if not (0 <= nr < rows and 0 <= nc < cols):
                break 
            if nr >= barrier_row_idx:
                break
                
            # Place trace '5'
            output_arr[nr, nc] = 5
            
            # Increment step counter
            k += 1

    # 7. Move Pattern (draw second, overwriting trace if necessary)
    moved_bounds = calculate_moved_bounds(original_bounds, cols, move_right)
    
    # Calculate column shift
    col_shift = moved_bounds['min_col'] - original_bounds['min_col']
    
    for r_orig, c_orig in original_coords:
        # Calculate destination coordinates
        tr, tc = r_orig, c_orig + col_shift
        
        # Draw the moved '5' if within bounds (should always be if moved_bounds is correct)
        if 0 <= tr < rows and 0 <= tc < cols:
             output_arr[tr, tc] = 5

    # 8. Place Markers (draw last, overwriting barrier '6's)
    if barrier_row_idx < rows: # Ensure barrier is within grid
        start_9_col = 0
        end_9_col = 0 # Inclusive end column index

        # Calculate marker range based on movement and bounds (derived from examples)
        if move_right:
            start_9_col = original_bounds['min_col']
            # The +1 on moved_bounds['min_col'] makes the end column inclusive and matches example 2
            end_9_col = moved_bounds['min_col'] + 1 
        else: # move_left
            # The +1 on moved_bounds['max_col'] makes the start column inclusive and matches example 1
            start_9_col = moved_bounds['max_col'] + 1 
            end_9_col = original_bounds['max_col']

        # Clip column indices to be within grid bounds [0, cols-1]
        start_9_col_clipped = max(0, start_9_col)
        end_9_col_clipped = min(cols - 1, end_9_col) 

        # Place markers if the clipped range is valid
        if start_9_col_clipped <= end_9_col_clipped:
             # Use end+1 for slicing as np slicing is exclusive at the end
             output_arr[barrier_row_idx, start_9_col_clipped : end_9_col_clipped + 1] = 9 

    # 9. Convert back to list of lists for the final output
    return output_arr.tolist()