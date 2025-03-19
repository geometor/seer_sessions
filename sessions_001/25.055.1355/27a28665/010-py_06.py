"""
1. Analyze the input grid and count the number of times adjacent pixels (up, down, left, right - not diagonal) have the same color, regardless of the specific color.
2. Handle edge cases: If the input grid is empty or has only one pixel, return 0.
3. Return the result.  The final output is a 1x1 grid containing this count.
"""

import numpy as np

def count_adjacent_same_color(grid):
    """
    Counts the number of adjacent (horizontally and vertically) pixels with the same color in a grid.
    """
    count = 0
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check adjacent cells (up, down, left, right)
            if r > 0 and grid[r - 1, c] == color:
                count += 1
            if r < rows - 1 and grid[r + 1, c] == color:
                count += 1
            if c > 0 and grid[r, c - 1] == color:
                count += 1
            if c < cols - 1 and grid[r, c + 1] == color:
                count += 1
    return count // 2  # Divide by 2 because each adjacency is counted twice

def transform(input_grid):
    # Convert input_grid to a NumPy array
    grid = np.array(input_grid)

    # Handle edge cases for empty or 1-pixel grids
    if grid.size == 0 or grid.size == 1:
        return [[0]]

    # Count all adjacent like colors
    adjacent_count = count_adjacent_same_color(grid)
    
    # The problem description requires the result be a 1 x 1 grid
    output_grid = [[adjacent_count]]

    return output_grid