```python
import numpy as np # Using numpy for easier slicing, though list comprehensions work too

"""
Identify a unique separator row and column composed of a single repeating digit (S). 
Based on the value of S, generate the output grid:
- If S is 1, extract the Top-Left quadrant (rows 0 to R-1, cols 0 to C-1).
- If S is 3, extract the Bottom-Left quadrant (rows R+1 to end, cols 0 to C-1).
- If S is 2, merge the Top-Left (TL) and Top-Right (TR) quadrants. The output has TL dimensions. 
  For each cell (r, c), the output value is the corresponding TR value (input_grid[r][c+C+1]) 
  unless the TR value is equal to S (2), in which case the TL value (input_grid[r][c]) is used.
"""

def find_separator_row(grid: list[list[int]]) -> tuple[int | None, int | None]:
    """Finds the row index and the repeated digit of the separator row."""
    for r_idx, row in enumerate(grid):
        if len(set(row)) == 1: # Check if all elements are the same
            return r_idx, row[0]
    return None, None # Should not happen based on problem description

def find_separator_col(grid: list[list[int]], expected_digit: int) -> int | None:
    """Finds the column index of the separator column with the expected digit."""
    num_rows = len(grid)
    num_cols = len(grid[0])
    for c_idx in range(num_cols):
        is_separator_col = True
        for r_idx in range(num_rows):
            if grid[r_idx][c_idx] != expected_digit:
                is_separator_col = False
                break
        if is_separator_col:
            return c_idx
    return None # Should not happen based on problem description

def extract_subgrid(grid: list[list[int]], row_slice: slice, col_slice: slice) -> list[list[int]]:
    """Extracts a subgrid defined by row and column slices."""
    # Convert to numpy array for easier slicing
    np_grid = np.array(grid, dtype=int)
    subgrid = np_grid[row_slice, col_slice]
    # Convert back to list of lists if necessary, or keep as numpy array
    return subgrid.tolist() 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on separator lines and digit.
    """
    
    # 1. Identify Separators
    separator_row_index, separator_digit = find_separator_row(input_grid)
    if separator_row_index is None or separator_digit is None:
        raise ValueError("Separator row not found.") # Or return empty/error state
        
    separator_col_index = find_separator_col(input_grid, separator_digit)
    if separator_col_index is None:
        raise ValueError("Separator column not found or digit mismatch.") # Or return empty/error state

    # Define R and C for clarity
    R = separator_row_index
    C = separator_col_index
    S = separator_digit
    num_rows = len(input_grid)
    num_cols = len(input_grid[0]) if num_rows > 0 else 0

    output_grid = []

    # 2. Determine Processing Rule based on Separator Digit (S)
    # 3. Generate Output Grid
    
    if S == 1:
        # Rule: Extract Top-Left quadrant
        # Rows from 0 up to R
        # Columns from 0 up to C
        row_slice = slice(0, R)
        col_slice = slice(0, C)
        output_grid = extract_subgrid(input_grid, row_slice, col_slice)
        
    elif S == 3:
        # Rule: Extract Bottom-Left quadrant
        # Rows from R + 1 to the end
        # Columns from 0 up to C
        row_slice = slice(R + 1, num_rows)
        col_slice = slice(0, C)
        output_grid = extract_subgrid(input_grid, row_slice, col_slice)
        
    elif S == 2:
        # Rule: Merge Top-Left (TL) and Top-Right (TR)
        # Define TL and TR coordinates
        tl_row_slice = slice(0, R)
        tl_col_slice = slice(0, C)
        tr_row_slice = slice(0, R)
        tr_col_slice = slice(C + 1, num_cols)

        # Get dimensions for output grid (same as TL)
        out_rows = R
        out_cols = C
        
        # Initialize output grid (can use numpy zeros or list comprehension)
        output_grid = [[0 for _ in range(out_cols)] for _ in range(out_rows)]

        # Iterate through each position (r, c) in the output grid's dimensions
        for r in range(out_rows):
            for c in range(out_cols):
                # Get value from corresponding TL position
                value_tl = input_grid[r][c]
                # Get value from corresponding TR position (adjusting column index)
                # Need check for TR bounds if grid isn't symmetrical, but examples are
                value_tr = input_grid[r][c + C + 1] 
                
                # Apply the merge rule
                if value_tr != S: # If TR value is not the separator digit
                    output_grid[r][c] = value_tr # Use TR value
                else: # Otherwise (if TR value is the separator digit)
                    output_grid[r][c] = value_tl # Use TL value
                    
    # else: # Handle potential future cases or errors for other S values
    #     raise ValueError(f"Unsupported separator digit: {S}")

    # 4. Return the generated output_grid
    return output_grid
```