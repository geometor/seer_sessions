import numpy as np
import copy

"""
Transformation Rule:

1. Identify the global smallest non-zero integer (R) and the global largest 
   non-zero integer (T) in the input grid.
2. If R or T cannot be found, or if R equals T, return the input grid unchanged.
3. Create a copy of the input grid for the output. Get the number of rows.
4. Process each column independently:
    a. Find the row index of the first occurrence of R (`first_r_row`). 
       If not found, skip the column.
    b. Check the blocking condition: If `first_r_row >= rows // 2`, skip the column.
    c. Find the row index of the first occurrence of T below `first_r_row` 
       (`first_t_below_r_row`). If not found, skip the column.
    d. Determine the replacement start row (`start_row`):
       - If `first_r_row == 1`, `start_row = first_t_below_r_row + 2`.
       - Otherwise, `start_row = first_t_below_r_row`.
    e. Apply replacements: Iterate from `start_row` to the end of the column. 
       If a cell in the input contains T, change the corresponding cell 
       in the output to R.
5. Return the modified output grid.
"""

def find_key_values(grid: np.ndarray) -> tuple[int | None, int | None]:
    """Finds the smallest (R) and largest (T) non-zero values in the grid."""
    non_zeros = grid[grid > 0]
    if non_zeros.size == 0:
        return None, None  # No non-zero numbers found
    
    min_val = np.min(non_zeros)
    max_val = np.max(non_zeros)
    
    # Handle case where only one unique non-zero value exists
    if min_val == max_val:
        return None, None 
        
    return min_val, max_val

def find_first_occurrence(arr: np.ndarray, value: int, start_row: int = 0) -> int | None:
    """Finds the row index of the first occurrence of 'value' in 'arr' starting from 'start_row'."""
    indices = np.where(arr[start_row:] == value)[0]
    if len(indices) > 0:
        return indices[0] + start_row # Adjust index relative to the original array
    return None

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Identify Global Key Values (R and T)
    r_val, t_val = find_key_values(input_np)

    # 2. Handle Edge Cases (no R/T or R==T)
    if r_val is None or t_val is None:
        return copy.deepcopy(input_grid) # Return a copy

    # 3. Initialize Output grid and get dimensions
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # 4. Process Each Column
    for j in range(cols):
        col_data = input_np[:, j]

        # 4a. Find First R
        first_r_row = find_first_occurrence(col_data, r_val)
        if first_r_row is None:
            continue # Skip column if R not found

        # 4b. Check Blocking Condition
        block_threshold = rows // 2
        if first_r_row >= block_threshold:
            continue # Skip column if first R is too low

        # 4c. Find First T Below R
        first_t_below_r_row = find_first_occurrence(col_data, t_val, start_row=first_r_row + 1)
        if first_t_below_r_row is None:
            continue # Skip column if no T found below the first R

        # 4d. Determine Replacement Start Row
        start_row: int
        if first_r_row == 1:
            start_row = first_t_below_r_row + 2
        else:
            start_row = first_t_below_r_row

        # 4e. Apply Replacements
        # Ensure start_row is within bounds before looping
        if start_row < rows:
            for i in range(start_row, rows):
                if input_np[i, j] == t_val:
                    output_np[i, j] = r_val

    # 5. Return Result
    return output_np.tolist()