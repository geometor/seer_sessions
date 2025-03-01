"""
The transformation extracts a 3x3 sub-grid from the input grid. The top-left corner of the sub-grid is determined by the first non-white (0) pixel encountered when scanning the input grid row by row. The output 3x3 grid contains non-zero pixel values arranged vertically and diagonally, maintaining their original relative positions.
"""

import numpy as np

def find_pivot(input_grid):
    # Iterate through rows and columns to find the first non-white pixel
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                return (r, c)
    return None  # Return None if no non-white pixel is found

def transform(input_grid):
    """
    Extracts a 3x3 subgrid from the input based on a pivot pixel and arranges
    non-zero pixels according to the observed pattern.
    """
    # Initialize a 3x3 output grid filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the pivot pixel (first non-white pixel)
    pivot = find_pivot(input_grid)

    if pivot is None:
        return output_grid  # Return empty grid if no pivot is found

    pivot_row, pivot_col = pivot
    
    rows, cols = input_grid.shape
    
    # Extract values for the output
    output_grid[0,2] = input_grid[pivot_row, pivot_col]
        
    # Check the same row for other non zero values to the right of the pivot
    for c in range(pivot_col + 1, cols):
        if input_grid[pivot_row,c] !=0:
            output_grid[0,2] = input_grid[pivot_row,c] # update pivot position
            break
            
    # Find values below the pivot position
    for r in range(pivot_row + 1, rows):
      if input_grid[r, pivot_col] != 0:
        output_grid[2,0] = input_grid[r,pivot_col]
        break

    return output_grid