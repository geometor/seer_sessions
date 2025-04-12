```python
import copy
import math

"""
Transforms a 2D grid based on patterns in its rows, with the transformation mode 
determined by the adjacency of non-zero elements in the last non-zero row.

1.  Find the last row containing non-zero elements (the 'reference row').
2.  Check if this reference row contains adjacent non-zero elements (at columns c and c+1).
3.  Mode A (Adjacent found): Transform each row independently based on its non-zero pattern.
    - Find non-zero cells `nz`, first/last columns (`c_min`, `c_max`), last value (`V`), 
      step between first two non-zeros, and if all non-zeros have the same value (`all_same_value`).
    - If fewer than 2 non-zeros, row is unchanged.
    - Apply filling:
        - If step=1 and all_same_value: Fill from c_min to end with V.
        - If step=1 and not all_same_value: Fill from c_min to c_max with V.
        - If step>1 and all_same_value: Fill every 'step' column from c_min to end with V.
        - If step>1 and not all_same_value: Fill every 'step' column from c_min up to c_max with V.
4.  Mode B (No adjacent found - Revised): Transform each row using the reference row as a base, with specific handling for all-zero input rows.
    - If the input row is all zeros, the output row is all zeros.
    - Otherwise:
        - Initialize the output row as a copy of the reference row data.
        - Place non-zero elements from the current input row onto the output row, overwriting reference values if necessary.
"""

# --- Helper Functions ---

def find_reference_info(grid: list[list[int]]) -> tuple[int | None, list[int] | None, list[tuple[int, int]] | None]:
    """
    Finds the index, data, and sorted non-zero elements (col, val) 
    of the last row containing non-zeros.
    Returns (None, None, None) if the grid is empty or all zeros.
    """
    ref_row_index = None
    ref_row_data = None
    ref_nz = None
    for r in range(len(grid) - 1, -1, -1):
        row = grid[r]
        nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
        if nz:
            ref_row_index = r
            ref_row_data = list(row) # Store a copy
            ref_nz = nz
            break
    return ref_row_index, ref_row_data, ref_nz

def check_adjacency(nz_list: list[tuple[int, int]]) -> bool:
    """
    Checks if any two consecutive elements in the sorted non-zero list 
    have column indices that differ by exactly 1.
    """
    if not nz_list or len(nz_list) < 2:
        return False
    for i in range(len(nz_list) - 1):
        if nz_list[i][0] + 1 == nz_list[i+1][0]:
            return True
    return False

def is_row_all_zeros(row: list[int]) -> bool:
    """Checks if all elements in a list are zero."""
    for x in row:
        if x != 0:
            return False
    return True

# --- Transformation Mode Functions ---

def transform_independent_row(input_row: list[int]) -> list[int]:
    """Applies the row-independent transformation logic (Mode A)."""
    nz = sorted([(c, val) for c, val in enumerate(input_row) if val != 0])
    row_width = len(input_row)
    output_row = list(input_row) # Start with a copy

    # If less than 2 non-zeros, no transformation needed for this row
    if len(nz) < 2:
        return output_row

    # Get properties for rows with >= 2 non-zero elements
    c_min = nz[0][0]
    c_max = nz[-1][0]
    V = nz[-1][1] # Value of the *last* non-zero element
    step = nz[1][0] - nz[0][0] # Difference between first two non-zero columns
    all_same_value = len(set(val for c, val in nz)) == 1

    # Apply filling logic based on step and value uniformity
    if step == 1:
        if all_same_value:
            # Fill from c_min to the end of the row
            for c in range(c_min, row_width):
                output_row[c] = V
        else:
            # Fill from c_min to c_max (inclusive)
            for c in range(c_min, c_max + 1):
                output_row[c] = V
    elif step > 1:
        c = c_min
        if all_same_value:
            # Fill every step-th column from c_min to end of row
            while c < row_width:
                output_row[c] = V
                c += step
        else:
            # Fill every step-th column from c_min up to c_max
            while c <= c_max:
                output_row[c] = V
                c += step
                
    return output_row

def transform_reference_overlay_row_revised(input_row: list[int], reference_row_data: list[int], width: int) -> list[int]:
    """Applies the revised reference row overlay transformation logic (Mode B - Revised)."""
    # Check if the current input row is all zeros
    if is_row_all_zeros(input_row):
        # If yes, return an all-zero row
        return [0] * width 
    else:
        # If input row has non-zeros, start with a copy of the reference row
        output_row = list(reference_row_data)
        # Overlay non-zeros from the current input row
        current_nz = [(c, val) for c, val in enumerate(input_row) if val != 0]
        for c, v in current_nz:
            if 0 <= c < width:
                output_row[c] = v
        return output_row

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid based on the adjacency rule of the last non-zero row.
    """
    # initialize output_grid
    output_grid = []
    
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []
        
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Find the reference row information
    ref_row_index, ref_row_data, ref_nz = find_reference_info(input_grid)

    # Handle case where grid is all zeros (no reference row found)
    if ref_row_index is None:
        return [list(row) for row in input_grid] # Return a copy

    # Determine the transformation mode based on adjacency in the reference row's non-zero elements
    mode_a = check_adjacency(ref_nz)

    # Perform transformations row by row based on the determined mode
    for r in range(num_rows):
        current_input_row = input_grid[r]
        if mode_a:
            # Mode A: Independent Row Transformation
            transformed_row = transform_independent_row(current_input_row)
        else:
            # Mode B: Reference Row Overlay (Revised)
            # Ensure ref_row_data is not None (shouldn't happen if ref_row_index is not None)
            if ref_row_data is None: 
                 # Fallback or error handling - perhaps return input row copy?
                 transformed_row = list(current_input_row) 
            else:
                transformed_row = transform_reference_overlay_row_revised(current_input_row, ref_row_data, num_cols)
                
        output_grid.append(transformed_row)

    return output_grid
```