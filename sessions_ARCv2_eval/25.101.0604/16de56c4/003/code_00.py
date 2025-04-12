import copy
import math

"""
Transforms a 2D grid based on patterns in its rows, governed by the structure of the last non-zero row.

1.  Find the last row in the input grid containing non-zero elements (the 'reference row').
2.  Check if this reference row contains any non-zero elements at adjacent column indices (c and c+1).
3.  If YES (adjacent non-zeros exist), apply 'Mode A' (Independent Row Transformation):
    - Transform each row independently.
    - For a row:
        - Find non-zero cells nz = [(c, v), ...].
        - If len(nz) < 2, keep the row as is.
        - Otherwise, find c_min, c_max, V (last value), step (diff between first two cols), all_same_value.
        - Copy the input row to output_row.
        - If all_same_value and step == 1: fill output_row from c_min to end with V.
        - Else if step == 1: fill output_row from c_min to c_max with V.
        - Else (step > 1): fill output_row[c] = V for c = c_min, c_min + step, ..., up to c_max.
4.  If NO (no adjacent non-zeros in reference row), apply 'Mode B' (Reference Row Overlay):
    - For each input row:
        - If the input row is all zeros, the output row is all zeros.
        - Otherwise:
            - Start with a copy of the reference row as the output_row.
            - Find non-zero cells (c, v) in the input row.
            - For each (c, v), set output_row[c] = v.
"""

def find_reference_info(grid: list[list[int]]) -> tuple[int | None, list[int] | None, list[tuple[int, int]] | None]:
    """Finds the index, data, and sorted non-zero elements of the last row containing non-zeros."""
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
    """Checks if any adjacent elements in the sorted non-zero list have consecutive column indices."""
    if not nz_list or len(nz_list) < 2:
        return False
    for i in range(len(nz_list) - 1):
        if nz_list[i][0] + 1 == nz_list[i+1][0]:
            return True
    return False

def transform_row_independent(row: list[int]) -> list[int]:
    """Applies the row-independent transformation logic (Mode A)."""
    # Find non-zero elements, sorted by column
    nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
    
    # Handle rows with 0 or 1 non-zero element: return unchanged copy
    if len(nz) < 2:
        return list(row) 

    # Get properties for rows with >= 2 non-zero elements
    c_min = nz[0][0]
    c_max = nz[-1][0]
    V = nz[-1][1] # Value of the *last* non-zero element
    step = nz[1][0] - nz[0][0] # Difference between first two non-zero columns
    all_same_value = len(set(val for c, val in nz)) == 1
    
    output_row = list(row) # Start with a copy of the input row
    row_width = len(row)

    # Apply filling logic based on conditions
    if all_same_value and step == 1:
        # Fill from c_min to the end of the row if adjacent and all same value
        for c in range(c_min, row_width):
            output_row[c] = V
    elif step == 1:
        # Fill from c_min to c_max (inclusive) if adjacent but different values
        for c in range(c_min, c_max + 1):
            output_row[c] = V
    elif step > 1:
        # Fill every step-th column starting from c_min, up to c_max
        c = c_min
        while c <= c_max: # Corrected boundary condition
            output_row[c] = V
            c += step
            
    return output_row

def transform_reference_overlay_grid(input_grid: list[list[int]], reference_row: list[int]) -> list[list[int]]:
    """Applies the reference row overlay transformation logic (Mode B)."""
    output_grid = []
    num_rows = len(input_grid)
    num_cols = len(input_grid[0]) if num_rows > 0 else 0
    
    for r in range(num_rows):
        current_row = input_grid[r]
        current_nz = [(c, val) for c, val in enumerate(current_row) if val != 0]
        
        # If the input row is all zeros, the output row is all zeros
        if not current_nz:
            output_grid.append([0] * num_cols) 
        else:
            # Start with a copy of the reference row
            output_row = list(reference_row)
            # Overlay non-zeros from the current input row
            for c, val in current_nz:
                 # Ensure column index is valid (safety check)
                 if 0 <= c < len(output_row):
                    output_row[c] = val
            output_grid.append(output_row)
            
    return output_grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on patterns in the last non-zero row.
    Chooses between two transformation types: 
    - Mode A: Independent row transformation (if last non-zero row has adjacent non-zeros).
    - Mode B: Reference row overlay (if last non-zero row has no adjacent non-zeros).
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []
        
    # Find the last non-zero row, its data, and its non-zero elements
    ref_row_index, ref_row_data, ref_nz = find_reference_info(input_grid)

    # If no non-zero elements exist anywhere in the grid, return a copy
    if ref_row_index is None:
        return [list(row) for row in input_grid] 

    # Determine the transformation mode by checking adjacency in the reference row
    has_adjacent = check_adjacency(ref_nz)

    # Apply Mode A (Independent Row Transformation)
    if has_adjacent:
        output_grid = []
        for r in range(len(input_grid)):
             output_grid.append(transform_row_independent(input_grid[r]))
        return output_grid
        
    # Apply Mode B (Reference Row Overlay)
    else:
        # Pass the actual data of the reference row
        return transform_reference_overlay_grid(input_grid, ref_row_data)