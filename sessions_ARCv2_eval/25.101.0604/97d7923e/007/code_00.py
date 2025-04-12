import numpy as np
import copy

"""
Transformation Rule:

1. Identify the global smallest non-zero integer (R) and the global largest 
   non-zero integer (T) in the input grid.
2. Initialize an output grid as a copy of the input. Get the number of rows.
3. Process each column independently:
    a. Check if the global minimum (R) exists in the current column.
    b. If R exists (Primary Rule):
        i. Find the row index of the first R (`first_r_row`).
        ii. Check blocking condition: if `first_r_row >= rows // 2`, skip this column.
        iii. Find the row index of the first T below `first_r_row` (`first_t_below_r_row`). If none, skip.
        iv. Determine start row: `start_row = first_t_below_r_row + 4` if `first_r_row == 1`, else `start_row = first_t_below_r_row`.
        v. Apply replacements: From `start_row` downwards, change T to R in the output grid.
    c. If R does NOT exist (Secondary Rule):
        i. Find the local minimum non-zero (`min_l`) and maximum non-zero (`max_l`) in the column.
        ii. If `min_l` and `max_l` exist and are different:
            * Find first `min_l`, last `min_l`, and first `max_l`.
            * If `first_min_l < first_max_l < last_min_l`, replace all `max_l` with `min_l` in the column in the output grid.
4. Return the modified output grid.
"""

def find_global_key_values(grid: np.ndarray) -> tuple[int | None, int | None]:
    """Finds the global smallest (R) and largest (T) non-zero values."""
    non_zeros = grid[grid > 0]
    if non_zeros.size == 0:
        return None, None
    min_val = np.min(non_zeros)
    max_val = np.max(non_zeros)
    return min_val, max_val

def find_local_key_values(column: np.ndarray) -> tuple[int | None, int | None]:
    """Finds the local smallest and largest non-zero values in a column."""
    non_zeros = column[column > 0]
    if non_zeros.size == 0:
        return None, None
    min_val = np.min(non_zeros)
    max_val = np.max(non_zeros)
    # Return None, None if only one unique non-zero value exists locally
    if min_val == max_val:
        return None, None
    return min_val, max_val

def find_first_occurrence(arr: np.ndarray, value: int, start_row: int = 0) -> int | None:
    """Finds the row index of the first occurrence of 'value' starting from 'start_row'."""
    indices = np.where(arr[start_row:] == value)[0]
    if len(indices) > 0:
        return indices[0] + start_row
    return None

def find_last_occurrence(arr: np.ndarray, value: int) -> int | None:
    """Finds the row index of the last occurrence of 'value'."""
    indices = np.where(arr == value)[0]
    if len(indices) > 0:
        return indices[-1]
    return None

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Convert input to numpy array
    input_np = np.array(input_grid, dtype=int)

    # 1. Identify Global Key Values (R and T)
    r_val_global, t_val_global = find_global_key_values(input_np)

    # 2. Initialize Output grid and get dimensions
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # If no global R or T, or they are the same, secondary rule might still apply,
    # but primary rule won't. We don't return early.

    # 3. Process Each Column
    for j in range(cols):
        col_data = input_np[:, j]
        
        # 3a. Check if Global R exists in the column
        r_present = r_val_global is not None and np.any(col_data == r_val_global)

        if r_present and r_val_global is not None and t_val_global is not None and r_val_global != t_val_global:
            # 3b. Apply Primary Rule
            
            # i. Find First R
            first_r_row = find_first_occurrence(col_data, r_val_global)
            # This check is redundant due to r_present, but good practice
            if first_r_row is None: 
                continue 

            # ii. Check Blocking Condition
            block_threshold = rows // 2
            if first_r_row >= block_threshold:
                continue

            # iii. Find First T Below R
            first_t_below_r_row = find_first_occurrence(col_data, t_val_global, start_row=first_r_row + 1)
            if first_t_below_r_row is None:
                continue

            # iv. Determine Replacement Start Row
            start_row: int
            if first_r_row == 1:
                start_row = first_t_below_r_row + 4 # Updated rule for first_r_row == 1
            else:
                start_row = first_t_below_r_row

            # v. Apply Replacements
            if start_row < rows:
                for i in range(start_row, rows):
                    if input_np[i, j] == t_val_global:
                        output_np[i, j] = r_val_global
        
        elif not r_present:
            # 3c. Apply Secondary Rule (Global R not in column)
            
            # i. Find Local Min/Max
            min_l, max_l = find_local_key_values(col_data)

            # ii. Check if valid local keys exist
            if min_l is not None and max_l is not None:
                # Find first min_l, last min_l, first max_l
                first_min_l_row = find_first_occurrence(col_data, min_l)
                last_min_l_row = find_last_occurrence(col_data, min_l)
                first_max_l_row = find_first_occurrence(col_data, max_l)

                # Check trigger condition: indices exist and are ordered correctly
                if (first_min_l_row is not None and 
                    last_min_l_row is not None and 
                    first_max_l_row is not None and
                    first_min_l_row < first_max_l_row and 
                    last_min_l_row > first_max_l_row):
                    
                    # Apply replacement: change all max_l to min_l
                    for i in range(rows):
                        if input_np[i, j] == max_l:
                            output_np[i, j] = min_l
                            
    # 4. Return Result
    return output_np.tolist()