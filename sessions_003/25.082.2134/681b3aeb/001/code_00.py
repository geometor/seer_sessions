"""
1. Start scanning the input grid, beginning at the top right corner (row 0,
   column 9). The search direction is first by column (right to left), then by
   row (top to bottom)
2. Find the first non-zero pixel.
3. Record this color.
4. Continue searching the grid in the same order (from top right to bottom left). Record the color of each non-zero pixel encountered.
5. Construct 3x3 output grid by filling the cells in order found colors.
6. Stop when the output grid is full.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.zeros((3, 3), dtype=int)
    colors = []

    # Iterate through the input grid from top-right to bottom-left
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1] - 1, -1, -1):
            color = input_grid[r, c]
            if color != 0:
                colors.append(color)

    # Fill the output grid with the found colors
    count = 0
    for r in range(3):
        for c in range(3):
            if count < len(colors):
                output_grid[r, c] = colors[count]
                count += 1
            else:
                break
        if count >= len(colors):
            break

    return output_grid