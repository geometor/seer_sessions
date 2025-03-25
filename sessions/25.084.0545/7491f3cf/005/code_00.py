"""
The transformation rule identifies lines of identical colors within a grid and extends them to the right (for horizontal lines) and down (for vertical lines), overwriting neighboring pixels. The extension continues until a boundary or a different color which isn't part of a similar line is encountered.
"""

import numpy as np

def is_horizontal_line(grid, row, col):
    """Checks if the pixel at (row, col) is the start of a horizontal line."""
    if col + 1 < len(grid[0]) and grid[row][col] == grid[row][col + 1]:
        return True
    return False

def is_vertical_line(grid, row, col):
    """Checks if the pixel at (row, col) is the start of a vertical line."""
    if row + 1 < len(grid) and grid[row][col] == grid[row + 1][col]:
        return True
    return False

def transform(input_grid):
    """
    Transforms the input grid according to the one-directional line extension rule,
    with extended overwriting.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid
    for i in range(rows):
        for j in range(cols):
            # Check for horizontal lines (extend to the right)
            if is_horizontal_line(input_grid, i, j):
                k = j + 1
                while k < cols:
                    if input_grid[i,k] == input_grid[i,j]:
                        k += 1
                        continue

                    
                    output_grid[i,k] = input_grid[i,j]
                    k+=1

            # Check for vertical lines (extend downwards)
            if is_vertical_line(input_grid, i, j):
                k = i + 1
                while k < rows:
                    if input_grid[k,j] == input_grid[i,j]:
                        k += 1
                        continue
                    
                    output_grid[k,j] = input_grid[i,j]
                    k+=1

    return output_grid.tolist()