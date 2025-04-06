import numpy as np

"""
Identify a separator row and column composed of a single repeating digit (S). 
Based on the value of S, extract a specific quadrant from the input grid, excluding the separator lines themselves.
If S is 1 or 2, extract the top-left quadrant. 
If S is 3, extract the bottom-left quadrant.
"""

def find_separator_row(grid: list[list[int]]) -> tuple[int | None, int | None]:
    """Finds the row index and the repeated digit of the separator row."""
    for r_idx, row in enumerate(grid):
        first_digit = row[0]
        if all(digit == first_digit for digit in row):
            return r_idx, first_digit
    return None, None # Should not happen based on problem description

def find_separator_col(grid: list[list[int]], expected_digit: int) -> int | None:
    """Finds the column index of the separator column with the expected digit."""
    num_rows = len(grid)
    num_cols = len(grid[0])
    for c_idx in range(num_cols):
        if all(grid[r_idx][c_idx] == expected_digit for r_idx in range(num_rows)):
            return c_idx
    return None # Should not happen based on problem description

def extract_subgrid(grid: list[list[int]], row_slice: slice, col_slice: slice) -> list[list[int]]:
    """Extracts a subgrid defined by row and column slices."""
    return [row[col_slice] for row in grid[row_slice]]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding separator lines and extracting a quadrant
    based on the separator digit.
    """
    
    # 1. Find the separator row and its digit
    separator_row_index, separator_digit = find_separator_row(input_grid)
    if separator_row_index is None or separator_digit is None:
        # Handle error: No separator row found (though problem implies one exists)
        return [] 
        
    # 2. Find the separator column using the same digit
    separator_col_index = find_separator_col(input_grid, separator_digit)
    if separator_col_index is None:
        # Handle error: No separator column found or digit mismatch
        return []

    # 3. Determine the quadrant to extract based on the separator digit
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    
    output_grid = []
    if separator_digit in [1, 2]:
        # Select Top-Left quadrant
        # Rows from 0 up to separator_row_index
        # Columns from 0 up to separator_col_index
        row_slice = slice(0, separator_row_index)
        col_slice = slice(0, separator_col_index)
        output_grid = extract_subgrid(input_grid, row_slice, col_slice)
        
    elif separator_digit == 3:
        # Select Bottom-Left quadrant
        # Rows from separator_row_index + 1 to the end
        # Columns from 0 up to separator_col_index
        row_slice = slice(separator_row_index + 1, num_rows)
        col_slice = slice(0, separator_col_index)
        output_grid = extract_subgrid(input_grid, row_slice, col_slice)
        
    # Add more conditions here if other separator digits map to other quadrants
    # else:
        # Handle unknown separator digit or unimplemented case
        # return [] 

    # 4. Return the extracted quadrant
    return output_grid