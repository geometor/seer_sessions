```python
import numpy as np
from typing import List, Tuple, Set

"""
1.  **Analyze Signal:** Examine the input grid for the number 7. Determine if 7s exist. If they do, identify:
    *   The set of all row indices containing at least one 7 (`rows_with_any_7`).
    *   The set of row indices containing *only* 7s (`rows_all_7`).
    *   Whether the first row (index 0) contains a 7 (`is_in_first_row`) and, if so, the minimum column index (`min_c_first_row`).
    *   Whether the last row (index H-1) contains a 7 (`is_in_last_row`) and, if so, the minimum column index (`min_c_last_row`).
    *   The overall minimum column index of any 7 (`min_c`).
2.  **Determine Transformation Mode:**
    *   **Mode None:** If no 7s are found in the grid.
    *   **Mode A:** If the set `rows_all_7` is not empty.
    *   **Mode B:** If Mode A is not met, AND (`is_in_first_row` is true OR `is_in_last_row` is true).
    *   **Mode C:** If Modes A and B are not met, but 7s exist in the grid (`rows_with_any_7` is not empty).
3.  **Execute Transformation based on Mode:**
    *   **If Mode None:** Return the input grid unchanged.
    *   **If Mode A:**
        a. Identify the set `R_all_7` (rows containing only 7s).
        b. Identify the set `R_sandwiched_1` (rows containing only 1s that are located vertically between any two rows from `R_all_7`).
        c. Construct the output grid by taking all rows from the input grid whose indices are *not* in `R_all_7` and *not* in `R_sandwiched_1`, maintaining their original relative order.
    *   **If Mode B:**
        a. Calculate the target output width `W_out`:
            i. If `min_c_last_row` exists and `min_c == min_c_last_row`: `W_out = min_c + 5`.
            ii. Else (implies `min_c_first_row` must exist): `W_out = min_c_first_row - 1`.
        b. Create an output grid structure with the same number of rows as the input and `W_out` columns.
        c. **Populate Content (Complex):** Fill the output grid. The content is derived from the first `W_out` columns of the input grid but involves context-specific modifications that go beyond simple 7-to-4 replacement. *The precise rules for these modifications are not fully determined.* The current implementation uses a tentative slice-and-replace (7->4) method.
    *   **If Mode C:**
        a. Identify the set `R_any_7` (all rows containing at least one 7).
        b. Create an intermediate grid by taking all rows from the input grid whose indices are *not* in `R_any_7`, maintaining their original relative order.
        c. **Modify and Extend (Complex):** Apply modifications to the content of this intermediate grid and extend its width by appending new columns to the right. *The rules for modification and the source/content of the appended columns are currently undetermined.* The current implementation only performs step 3.c.a.
4.  **Return Output:** Return the resulting grid based on the executed mode.
"""


# --- Helper Functions ---

def find_value_coords(grid: np.ndarray, value: int) -> List[Tuple[int, int]]:
    """Finds all (row, col) coordinates of cells containing the specified value."""
    rows, cols = np.where(grid == value)
    return list(zip(rows, cols))

def is_row_all_value(row: np.ndarray, value: int) -> bool:
    """Checks if a 1D numpy array (a row) contains only the specified value."""
    # Ensure row is not empty before checking all elements
    return row.size > 0 and np.all(row == value)

def find_sandwiched_rows(grid: np.ndarray, value_to_find: int, sandwiching_row_indices: Set[int]) -> Set[int]:
    """
    Finds indices of rows that contain only `value_to_find` and are
    vertically strictly between rows specified by `sandwiching_row_indices`.
    """
    sandwiched_indices = set()
    # Need at least two sandwiching rows to have anything in between
    if len(sandwiching_row_indices) < 2:
        return sandwiched_indices

    # Sort the sandwiching row indices to find the min and max range
    sorted_sandwich_indices = sorted(list(sandwiching_row_indices))
    min_sandwich_r = sorted_sandwich_indices[0]
    max_sandwich_r = sorted_sandwich_indices[-1]

    # Iterate through rows strictly between the outer sandwiching rows
    for r_idx in range(min_sandwich_r + 1, max_sandwich_r):
        # Check if the row itself is one of the sandwiching rows (should not happen in this range, but safe check)
        if r_idx in sandwiching_row_indices:
            continue

        # Check if the row contains only the target value (e.g., 1)
        if is_row_all_value(grid[r_idx, :], value_to_find):
            # Check if there exists *some* sandwiching row above it and *some* below it.
            # This condition is implicitly met since we are looping between min_sandwich_r and max_sandwich_r.
            # We also need to ensure it's not adjacent only to the min or max without another sandwiching row on the other side.
            # The easiest way is just to check if it's between *any* two sandwiching rows.
            is_sandwiched = False
            for r1 in sorted_sandwich_indices:
                for r2 in sorted_sandwich_indices:
                    if r1 < r_idx < r2:
                        is_sandwiched = True
                        break
                if is_sandwiched:
                    break
            
            if is_sandwiched:
                sandwiched_indices.add(r_idx)

    return sandwiched_indices


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the presence and location of the number 7.
    """
    # Handle empty input
    if not input_grid or not input_grid[0]:
        return []

    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    output_grid_np = None

    # --- 1. Analyze Signal ---
    coords_7 = find_value_coords(grid, 7)
    rows_with_any_7 = set(r for r, c in coords_7)

    # Check if any 7s exist at all
    if not coords_7:
        # --- Mode None: No 7s ---
        # Return input grid unchanged
        return input_grid

    # Check for rows consisting entirely of 7s
    rows_all_7 = set()
    for r_idx in range(height):
        if is_row_all_value(grid[r_idx, :], 7):
            rows_all_7.add(r_idx)

    # Check for 7s in first and last rows and find min column indices
    is_in_first_row = 0 in rows_with_any_7
    is_in_last_row = (height - 1) in rows_with_any_7

    # Use float('inf') as default for min operations if no 7s found in specific rows
    min_c = min(c for r, c in coords_7) # Overall min column index for any 7
    min_c_first_row = min((c for r, c in coords_7 if r == 0), default=float('inf'))
    min_c_last_row = min((c for r, c in coords_7 if r == height - 1), default=float('inf'))

    # --- 2. Determine Transformation Mode ---
    mode = None
    if rows_all_7:
        mode = 'A'
    elif is_in_first_row or is_in_last_row:
        mode = 'B'
    else:
        # 7s exist, but not satisfying A or B criteria
        mode = 'C'

    # --- 3. Execute Transformation based on Mode ---
    if mode == 'A':
        # Identify rows consisting entirely of 1s sandwiched between all-7 rows
        sandwiched_1_rows = find_sandwiched_rows(grid, 1, rows_all_7)

        # Rows to remove are the all-7 rows plus the sandwiched '1' rows
        rows_to_remove = rows_all_7.union(sandwiched_1_rows)

        # Keep rows whose indices are not in the removal set
        rows_to_keep = [r for r in range(height) if r not in rows_to_remove]

        # Construct output grid
        if not rows_to_keep:
             output_grid_np = np.empty((0, width), dtype=int) # Return empty grid if all rows removed
        else:
             output_grid_np = grid[rows_to_keep, :]

    elif mode == 'B':
        # Calculate target output width W_out based on boundary 7 positions
        W_out = -1 # Default invalid width
        if min_c_last_row != float('inf') and min_c == min_c_last_row:
             # Condition derived from Example 2 analysis
             W_out = min_c + 5
        elif min_c_first_row != float('inf'):
             # Condition derived from Example 1 analysis
             W_out = min_c_first_row - 1
        else:
            # Fallback: This case shouldn't be reached if Mode B was triggered correctly.
            # If it somehow is, maybe default to min_c crop? Or handle as error?
            # Using min_c is a guess.
            W_out = min_c

        # Ensure W_out is non-negative
        W_out = max(0, W_out)

        # Create output grid by slicing and performing TENTATIVE modification
        if W_out >= 0:
            # Take the first W_out columns
            temp_grid = grid[:, :W_out].copy()
            # Replace 7s with 4s in the sliced grid
            # !!! NOTE: This content generation rule is known to be incomplete/inaccurate
            # !!! based on examples 1 & 2. The actual modification is more complex.
            temp_grid[temp_grid == 7] = 4
            output_grid_np = temp_grid
        else:
             # Should not happen with max(0, W_out), but handles potential edge case
             output_grid_np = np.empty((height, 0), dtype=int)

    elif mode == 'C':
        # Identify all rows containing any 7
        rows_to_remove = rows_with_any_7

        # Keep rows whose indices are not in the removal set
        rows_to_keep = [r for r in range(height) if r not in rows_to_remove]

        # Construct intermediate grid (only row removal performed)
        if not rows_to_keep:
             output_grid_np = np.empty((0, width), dtype=int)
        else:
             output_grid_np = grid[rows_to_keep, :]
             # !!! NOTE: Modification and width extension logic for Mode C is missing.
             # !!! The actual output for Mode C (e.g., Example 4) requires further
             # !!! processing on this intermediate grid.


    # --- 4. Return Output ---
    if output_grid_np is None:
        # This should ideally not happen if a mode was assigned and executed
        return [] # Return empty list as a fallback

    # Convert numpy array back to list of lists
    output_list = output_grid_np.tolist()

    # Handle cases where output grid became empty due to operations
    if output_grid_np.size == 0:
        if output_grid_np.shape[0] > 0 and output_grid_np.shape[1] == 0:
            # Case: Cropped to zero width (Mode B potentially)
             return [[] for _ in range(output_grid_np.shape[0])]
        elif output_grid_np.shape[0] == 0:
            # Case: All rows removed (Mode A or C potentially)
             return []
        # Includes case shape (0,0) - return empty list
        return []

    return output_list
```