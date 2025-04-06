import math

"""
Transforms an input grid of integers based on repetition patterns.

1. Checks for vertical repetition: If the number of rows (N) is even and the top half of the rows is identical to the bottom half, the output is the top half.
2. If no vertical repetition is found (or N is odd), checks for horizontal repetition: If the number of columns (M) in each row is even and the left half of each row is identical to its right half for *all* rows, the output consists of the left half of each row.
3. If neither repetition pattern is detected, the original input grid is returned (as a fallback, though examples imply a pattern will exist).
"""

def _split_vertically(grid: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    """Splits the grid vertically into two halves."""
    n_rows = len(grid)
    midpoint = n_rows // 2
    top_half = grid[:midpoint]
    bottom_half = grid[midpoint:]
    return top_half, bottom_half

def _split_horizontally(row: list[int]) -> tuple[list[int], list[int]]:
    """Splits a single row horizontally into two halves."""
    n_cols = len(row)
    midpoint = n_cols // 2
    left_half = row[:midpoint]
    right_half = row[midpoint:]
    return left_half, right_half

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists of integers representing the input grid.

    Returns:
        A list of lists of integers representing the transformed output grid.
    """
    
    n_rows = len(input_grid)

    # 1. Check for Vertical Repetition
    if n_rows > 0 and n_rows % 2 == 0:
        top_half, bottom_half = _split_vertically(input_grid)
        # Compare the top and bottom blocks
        if top_half == bottom_half:
            # If identical, output is the top block
            return top_half

    # 2. Check for Horizontal Repetition (if vertical repetition was not found or N is odd)
    # Assume consistent number of columns for horizontal check based on the first row
    if n_rows > 0:
        n_cols = len(input_grid[0]) if input_grid else 0 # Handle empty grid case
        
        # Check if columns are even and > 0 for potential horizontal split
        if n_cols > 0 and n_cols % 2 == 0:
            all_lines_repeat_horizontally = True
            output_grid_horizontal = []

            # Iterate through each line
            for row in input_grid:
                 # Check consistency of columns and if splitting is possible
                 if len(row) != n_cols:
                     all_lines_repeat_horizontally = False # Rows have different lengths, cannot apply horizontal rule consistently
                     break 
                 
                 left_half, right_half = _split_horizontally(row)
                 # Compare left and right halves
                 if left_half != right_half:
                     all_lines_repeat_horizontally = False
                     break # Stop checking rows if one doesn't repeat
                 else:
                     # Store the left half for potential output
                     output_grid_horizontal.append(left_half)

            # If all lines had horizontal repetition
            if all_lines_repeat_horizontally:
                return output_grid_horizontal

    # 3. No repetition pattern detected (or input conditions not met for checks)
    # Return the original grid as a fallback
    return input_grid
