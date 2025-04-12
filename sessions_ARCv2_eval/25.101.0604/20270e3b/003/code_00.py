import numpy as np
from typing import List, Tuple, Set

"""
The transformation rule operates based on the presence and configuration of the number 7 within the input grid. It distinguishes between three primary modes:

1.  **Analyze Signal:** Examine the input grid to find all occurrences of the number 7. Determine the following properties:
    *   Does any row consist entirely of 7s?
    *   Are there any 7s in the first row (row 0)? If yes, find the minimum column index (`min_c_first_row`).
    *   Are there any 7s in the last row (row H-1)? If yes, find the minimum column index (`min_c_last_row`).
    *   Find the overall minimum column index (`min_c`) where any 7 appears.
2.  **Determine Transformation Mode:**
    *   **Mode A:** If any row consists entirely of 7s.
    *   **Mode B:** If Mode A is not met, AND (there is a 7 in the first row OR there is a 7 in the last row).
    *   **Mode C:** If Mode A and Mode B are not met, but 7s are present in the grid.
    *   **(Default):** If no 7s are present, return the input grid unchanged.
3.  **Execute Transformation based on Mode:**
    *   **If Mode A:**
        a. Identify the set of indices `R_all_7` for all rows containing only 7s.
        b. Identify the set of indices `R_sandwiched_1` for all rows that contain only 1s and are located vertically between any two rows whose indices are in `R_all_7`.
        c. Construct the output grid by selecting all rows from the input grid whose indices are *not* in `R_all_7` and *not* in `R_sandwiched_1`, maintaining their original relative order.
    *   **If Mode B:**
        a. Calculate the target output width `W_out`:
            i. If `min_c == min_c_last_row` (and `min_c_last_row` is finite): `W_out = min_c + 5`.
            ii. Otherwise (meaning `min_c != min_c_last_row` or `min_c_last_row` is infinite, implies `min_c_first_row` must be relevant): `W_out = min_c_first_row - 1`.
        b. Construct the output grid with the original number of rows and `W_out` columns.
        c. **(Content Generation - Tentative):** Populate the output grid by taking the first `W_out` columns of the input grid and replacing any 7s found within this subgrid with 4s. *(Note: This content generation is a simplified hypothesis and likely incomplete based on example outputs.)*
    *   **If Mode C:**
        a. Identify the set of indices `R_any_7` for all rows containing at least one 7.
        b. Create an intermediate grid by selecting all rows from the input grid whose indices are *not* in `R_any_7`, maintaining original relative order.
        c. **(Modification and Extension - Missing):** The logic for modifying the content and extending the width of this intermediate grid is currently unknown and not implemented. The function currently returns only the result of step 3.c.a.
4.  **Return Output:** Return the resulting grid.
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
    return row.size > 0 and np.all(row == value)

def find_sandwiched_rows(grid: np.ndarray, value_to_find: int, sandwiching_row_indices: Set[int]) -> Set[int]:
    """
    Finds indices of rows that contain only `value_to_find` and are
    vertically sandwiched between rows specified by `sandwiching_row_indices`.
    """
    sandwiched_indices = set()
    if not sandwiching_row_indices:
        return sandwiched_indices

    sorted_sandwich_indices = sorted(list(sandwiching_row_indices))
    min_sandwich_r = sorted_sandwich_indices[0]
    max_sandwich_r = sorted_sandwich_indices[-1]

    for r_idx in range(min_sandwich_r + 1, max_sandwich_r):
        # Check if the row itself is one of the sandwiching rows
        if r_idx in sandwiching_row_indices:
            continue

        # Check if the row contains only the target value (e.g., 1)
        if is_row_all_value(grid[r_idx, :], value_to_find):
            # Check if there exists a sandwiching row strictly above and strictly below it
            # Since we iterate between min and max sandwich rows, this is implicitly true
            # if the row is not itself a sandwiching row.
             sandwiched_indices.add(r_idx)

    return sandwiched_indices


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Handle empty input
    if not input_grid or not input_grid[0]:
        return []

    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    output_grid_np = None

    # 1. Analyze Signal
    coords_7 = find_value_coords(grid, 7)
    rows_with_any_7 = set(r for r, c in coords_7)

    # Check if any 7s exist at all
    if not coords_7:
        # Default: No 7s, return input grid unchanged
        return input_grid

    # Check for rows consisting entirely of 7s
    rows_all_7 = set()
    for r_idx in range(height):
        if is_row_all_value(grid[r_idx, :], 7):
            rows_all_7.add(r_idx)

    # Check for 7s in first and last rows and find min column indices
    has_7_first_row = 0 in rows_with_any_7
    has_7_last_row = (height - 1) in rows_with_any_7

    min_c = min(c for r, c in coords_7) if coords_7 else float('inf')
    min_c_first_row = min((c for r, c in coords_7 if r == 0), default=float('inf'))
    min_c_last_row = min((c for r, c in coords_7 if r == height - 1), default=float('inf'))

    # 2. Determine Transformation Mode
    mode = None
    if rows_all_7:
        mode = 'A'
    elif has_7_first_row or has_7_last_row:
        mode = 'B'
    else:
        # 7s exist, but not satisfying A or B
        mode = 'C'

    # 3. Execute Transformation based on Mode
    if mode == 'A':
        # Identify rows consisting entirely of 1s sandwiched between all-7 rows
        sandwiched_1_rows = find_sandwiched_rows(grid, 1, rows_all_7)

        # Rows to remove are the all-7 rows plus the sandwiched '1' rows
        rows_to_remove = rows_all_7.union(sandwiched_1_rows)

        # Keep rows whose indices are not in the removal set
        rows_to_keep = [r for r in range(height) if r not in rows_to_remove]

        if not rows_to_keep:
             output_grid_np = np.empty((0, width), dtype=int)
        else:
             output_grid_np = grid[rows_to_keep, :]

    elif mode == 'B':
        # Calculate target output width W_out
        W_out = -1 # Default invalid width
        # The check `min_c == min_c_last_row` seems too specific, let's adjust based on example outputs:
        # Example 1: min_c=3, min_c_first_row=9, min_c_last_row=inf => W_out = min_c_first_row - 1 = 8 ?
        # Example 2: min_c=1, min_c_first_row=10, min_c_last_row=1 => W_out = min_c + 5 = 6 ?

        if min_c_last_row != float('inf') and min_c == min_c_last_row:
             # This condition seems to match Example 2
             W_out = min_c + 5
        elif min_c_first_row != float('inf'):
             # This condition seems to match Example 1
             W_out = min_c_first_row - 1
        else:
            # Fallback or error case - should not happen if Mode B is triggered
            # Let's default to the simpler previous logic as a safety net, although known to be wrong
             W_out = min_c

        # Ensure W_out is non-negative
        W_out = max(0, W_out)

        # Create output grid by slicing and modifying
        if W_out >= 0:
            # Take the first W_out columns
            temp_grid = grid[:, :W_out].copy()
            # Replace 7s with 4s in the sliced grid (Tentative content rule)
            temp_grid[temp_grid == 7] = 4
            output_grid_np = temp_grid
        else:
            # Should not happen with max(0, W_out)
            output_grid_np = np.empty((height, 0), dtype=int)


    elif mode == 'C':
        # Identify all rows containing any 7
        rows_to_remove = rows_with_any_7

        # Keep rows whose indices are not in the removal set
        rows_to_keep = [r for r in range(height) if r not in rows_to_remove]

        if not rows_to_keep:
             output_grid_np = np.empty((0, width), dtype=int)
        else:
             output_grid_np = grid[rows_to_keep, :]
             # >>> Modification and Extension logic is missing here for Mode C <<<
             # The current output for Mode C will only have rows removed.


    # 4. Return Output
    if output_grid_np is None:
        # Should not happen if one of the modes was executed
        return [] # Return empty list if something went wrong

    # Convert numpy array back to list of lists
    output_list = output_grid_np.tolist()

    # Handle cases where output became empty
    if output_grid_np.size == 0:
        if output_grid_np.shape[0] > 0 and output_grid_np.shape[1] == 0:
            # Cropped to zero width, return list of empty lists
             return [[] for _ in range(output_grid_np.shape[0])]
        elif output_grid_np.shape[0] == 0:
            # All rows removed
             return []
        else: # Should cover shape (0,0)
            return []


    return output_list