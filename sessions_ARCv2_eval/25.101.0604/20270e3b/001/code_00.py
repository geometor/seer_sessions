import numpy as np
from typing import List, Tuple, Set

"""
The transformation rule distinguishes between two primary modes based on the location of the number 7 in the input grid.

1.  **Analyze Signal:** Identify all cells containing the number 7.
2.  **Determine Operation Mode:**
    *   **Mode A (Row Removal):** If no 7s are present in the first row (row 0) or the last row.
    *   **Mode B (Column Crop):** If any 7 is present in the first row or the last row.
3.  **Execute Operation:**
    *   **If Mode A:**
        a. Identify the set of row indices `R_7` that contain at least one 7.
        b. Identify the set of row indices `R_1_sandwiched` corresponding to rows that:
            i. Consist entirely of the number 1.
            ii. Are located strictly between two rows whose indices are in `R_7`. (e.g., row `r` is sandwiched if `r1 < r < r2` for some `r1, r2` in `R_7`, and row `r` contains only 1s).
        c. Construct the output grid by keeping all rows from the input grid whose indices are *not* in `R_7` and *not* in `R_1_sandwiched`, maintaining their original relative order.
        d. (Note: The extension observed in train_4 is not implemented in this version).
    *   **If Mode B:**
        a. Find the minimum column index `min_c` where a 7 appears in *any* row.
        b. Construct the output grid by taking only the first `min_c` columns from each row of the *original* input grid.
        c. (Note: This is a simplified interpretation for Mode B based on observations; it doesn't perfectly match train_1 and train_2 outputs and needs refinement).
4.  **Final Output:** The grid resulting from the selected operation mode.
"""

def find_value_coords(grid: np.ndarray, value: int) -> List[Tuple[int, int]]:
    """Finds all (row, col) coordinates of cells containing the specified value."""
    rows, cols = np.where(grid == value)
    return list(zip(rows, cols))

def get_rows_with_value(grid: np.ndarray, value: int) -> Set[int]:
    """Returns a set of row indices that contain the specified value."""
    coords = find_value_coords(grid, value)
    return set(r for r, c in coords)

def is_row_all_value(row: np.ndarray, value: int) -> bool:
    """Checks if a 1D numpy array (a row) contains only the specified value."""
    return np.all(row == value)

def find_sandwiched_rows(grid: np.ndarray, value_to_find: int, sandwiching_row_indices: Set[int]) -> Set[int]:
    """
    Finds indices of rows that contain only `value_to_find` and are
    vertically sandwiched between rows specified by `sandwiching_row_indices`.
    """
    sandwiched_indices = set()
    if not sandwiching_row_indices:
        return sandwiched_indices

    sorted_sandwich_indices = sorted(list(sandwiching_row_indices))
    
    for r_idx in range(grid.shape[0]):
        # Check if the row itself is one of the sandwiching rows
        if r_idx in sandwiching_row_indices:
            continue
            
        # Check if the row contains only the target value (e.g., 1)
        if is_row_all_value(grid[r_idx, :], value_to_find):
            # Check if there exists a sandwiching row above and below it
            has_above = any(sr < r_idx for sr in sorted_sandwich_indices)
            has_below = any(sr > r_idx for sr in sorted_sandwich_indices)
            
            if has_above and has_below:
                sandwiched_indices.add(r_idx)
                
    return sandwiched_indices

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the presence and location of the number 7.
    """
    if not input_grid or not input_grid[0]:
        return []
        
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # 1. Analyze Signal
    coords_7 = find_value_coords(grid, 7)
    rows_with_7 = set(r for r, c in coords_7)

    # 2. Determine Operation Mode
    mode = 'A' # Default to Row Removal
    if height > 0:
        # Check first row (index 0) and last row (index height-1)
        if 0 in rows_with_7 or (height - 1) in rows_with_7:
            mode = 'B' # Column Crop mode if 7 is in boundary rows

    output_grid_np = None

    # 3. Execute Operation
    if mode == 'B':
        # Mode B: Column Crop (Simplified version)
        if not coords_7: # Should not happen if mode B is triggered, but handle defensively
             output_grid_np = grid # No 7s, return original? Or handle based on problem spec. Assume return original for now.
        else:
            min_c = min(c for r, c in coords_7)
            # Take the first 'min_c' columns
            output_grid_np = grid[:, :min_c]
            
    else: # mode == 'A'
        # Mode A: Row Removal
        
        # Identify rows consisting entirely of 1s sandwiched between rows containing 7s
        sandwiched_1_rows = find_sandwiched_rows(grid, 1, rows_with_7)
        
        # Rows to remove are those with 7s plus the sandwiched '1' rows
        rows_to_remove = rows_with_7.union(sandwiched_1_rows)
        
        # Keep rows whose indices are not in the removal set
        rows_to_keep = [r for r in range(height) if r not in rows_to_remove]
        
        if not rows_to_keep:
             output_grid_np = np.empty((0, width), dtype=int) # Return empty grid if all rows removed
        else:
             output_grid_np = grid[rows_to_keep, :]
             # Note: Extension logic for train_4 (Mode C) is not implemented here.

    # 4. Final Output
    # Convert numpy array back to list of lists
    if output_grid_np is None: # Should ideally not happen with current logic
        return []
        
    output_list = output_grid_np.tolist()
    
    # Handle case where output is empty (e.g., all rows removed or cropped to zero width)
    if output_grid_np.size == 0 and output_grid_np.shape[1] > 0: # Rows removed, keep original width structure for empty list
         return []
    elif output_grid_np.size == 0 and output_grid_np.shape[1] == 0: # Cropped to zero width
        # Return list of empty lists, one for each kept row
        return [[] for _ in range(output_grid_np.shape[0])]
        
    return output_list