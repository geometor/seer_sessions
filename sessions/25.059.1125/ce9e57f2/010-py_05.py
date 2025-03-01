"""
1. Identify "red stacks": Find vertical stacks of red (2) pixels. A "red stack" is defined as two or more contiguous red pixels, where each pixel (except the topmost) is directly below another red pixel.
2. Transform bottom pixels: The bottom two pixels of each "red stack" are changed from red (2) to azure (8).
3. Preserve other pixels: All other pixels in the grid retain their original colors.
"""

import numpy as np

def find_red_stacks(grid):
    """Finds vertical stacks of red pixels in the grid."""
    rows, cols = grid.shape
    red_stacks = []
    for j in range(cols):
        stack = []
        for i in range(rows):
            if grid[i, j] == 2:
                stack.append((i, j))
            else:
                if len(stack) >= 2:
                    red_stacks.append(stack)
                stack = []
        # Check for stacks at the end of a column
        if len(stack) >= 2:
            red_stacks.append(stack)
    return red_stacks

def transform(input_grid):
    """Transforms red stacks in the input grid to azure at the bottom."""
    output_grid = np.copy(input_grid)
    red_stacks = find_red_stacks(output_grid)

    for stack in red_stacks:
        # Change the bottom two pixels of each stack to azure (8)
        if len(stack) >= 2:
          output_grid[stack[-1]] = 8  # Bottom-most pixel
          output_grid[stack[-2]] = 8  # Second-to-bottom pixel

    return output_grid