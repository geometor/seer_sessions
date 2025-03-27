"""
1.  **Identify Connected Components:** Find all connected components (groups of adjacent pixels of the same color).
2.  **Process Gray/Magenta:**
    - Examine each pixel within gray (5) or magenta (6) colored components.
    - **Magenta Block Rule**: If a magenta pixel is part of a 2x2 block or larger, it turns gray.
    - **Magenta/Gray Removal:** If a magenta/gray pixel is connected to white pixels vertically or horizontally, remove it (change to white).
"""

import numpy as np
from scipy.ndimage import measurements

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors


def is_part_of_2x2_block(grid, row, col, color):
    """Checks if a pixel is part of a 2x2 or larger block of the same color."""
    if grid[row, col] != color:
        return False

    rows, cols = grid.shape
    # Check for a 2x2 block in all possible directions
    if (row + 1 < rows and col + 1 < cols and
        grid[row + 1, col] == color and
        grid[row, col + 1] == color and
        grid[row + 1, col + 1] == color):
        return True
    if (row -1 >= 0 and col + 1 < cols and
        grid[row-1, col] == color and
        grid[row, col+1] == color and
        grid[row-1, col+1] == color):
        return True
    if (row -1 >= 0 and col -1 >= 0 and
        grid[row-1, col] == color and
        grid[row, col-1] == color and
        grid[row-1, col-1] == color):
        return True
    if(row + 1 < rows and col -1 >= 0 and
        grid[row+1, col] == color and
        grid[row, col - 1] == color and
        grid[row+1,col-1] == color):
        return True


    return False


def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all pixels
    for row in range(rows):
        for col in range(cols):
            # Magenta Block Rule
            if input_grid[row, col] == 6:  # Magenta
                if is_part_of_2x2_block(input_grid, row, col, 6):
                    output_grid[row, col] = 5  # Change to gray

    # Iterate a second time.  This is required because the 2x2 check can modify
    # the grid, need to do the gray/magenta removal *after*
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] in (5, 6):
                neighbors = get_neighbors(output_grid, row, col)
                for r, c in neighbors:
                    if output_grid[r,c] == 0:
                        output_grid[row,col] = 0
                        break

    return output_grid