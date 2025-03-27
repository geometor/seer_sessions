"""
1. Identify Seed Pixels: Find all pixels in the input grid with a non-zero color value. These are the "seed pixels."

2. Horizontal Extension: For each seed pixel:
    *   Extend the color of the seed pixel to all pixels to its right in the same row, until the edge of the grid is reached. This forms a horizontal segment of the same color.

3. Identify Rightmost Pixels: For each row and horizontal color segment in the *output grid*, find the rightmost pixel of that segment. The rightmost pixel marks the end of each horizontal extension created in step 2.

4. Vertical Extension: For each rightmost pixel identified in step 3:
    *   Extend the color of the rightmost pixel downwards to all pixels in the same column, until the edge of the grid is reached.
"""

import numpy as np

def find_rightmost(row, start_col, color):
    """Finds the rightmost pixel of the given color in a row, starting from start_col."""
    rightmost = start_col
    for i in range(start_col + 1, len(row)):
        if row[i] == color:
            rightmost = i
        else:
            break  # Stop when a different color or 0 is encountered
    return rightmost

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Horizontal Extension
    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] != 0:  # Seed pixel found
                for k in range(j, cols):
                    output_grid[i][k] = input_grid[i][j]

    # Identify Rightmost Pixels and Vertical Extension
    for i in range(rows):
        for j in range(cols):
            if output_grid[i][j] != 0:
                color = output_grid[i][j]
                rightmost = find_rightmost(output_grid[i], j, color)
                # Vertical Extension (only from the rightmost pixel)
                for r in range(i + 1, rows):
                    output_grid[r][rightmost] = output_grid[i][rightmost]
                j = rightmost #skip to the next segment

    return output_grid