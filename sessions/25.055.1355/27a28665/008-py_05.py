"""
1. Count the occurrences of the most frequent color. Analyze the input grid and identify the color that appears most frequently, excluding white (0).
2. Count adjacent like colors. For the most frequent color, find occurrences where adjacent vertical and horizontal (not diagonal) pixels are the same color
3. Return the result. The final output is the result of the counting.
"""

import numpy as np

def count_adjacent_same_color(grid, color):
    count = 0
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
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
    # Convert input_grid to a NumPy array for easier manipulation
    grid = np.array(input_grid)

    # Find the most frequent color, excluding 0 (white)
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    
    if 0 in color_counts:
        del color_counts[0] #delete white

    if not color_counts:
        return [[0]] #if no other colors, return 0

    most_frequent_color = max(color_counts, key=color_counts.get)

    # Count adjacent like colors
    adjacent_count = count_adjacent_same_color(grid, most_frequent_color)
    
    # the problem description requires the result be a 1 x 1 grid
    output_grid = [[adjacent_count]]
    return output_grid