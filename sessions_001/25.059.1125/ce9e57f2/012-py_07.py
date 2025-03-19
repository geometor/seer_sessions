"""
1. Identify Red Stacks: Find all vertical stacks of red (2) pixels. A "red stack" is a contiguous set of one or more red pixels in a single column, where each pixel (except possibly the top one) is directly below another red pixel.
2. Categorize Stacks by Height: Determine the height (number of pixels) of each red stack.
3. Apply Height-Based Transformation:
    - If the stack height is 1: No change occurs.
    - If the stack height is 2: Change only the bottom pixel of the stack to azure (8).
    - If the stack height is 3 or more: Change the bottom two pixels of the stack to azure (8).
4. Preserve Other Pixels: All pixels that are not part of a red stack, and red stack pixels not affected by step 3, maintain their original colors.
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
                if len(stack) > 0:
                    red_stacks.append(stack)
                stack = []
        # Check for stacks at the end of a column
        if len(stack) > 0:
            red_stacks.append(stack)
    return red_stacks

def transform(input_grid):
    """Transforms red stacks in the input grid based on their height."""
    output_grid = np.copy(input_grid)
    red_stacks = find_red_stacks(output_grid)

    for stack in red_stacks:
        stack_height = len(stack)
        # Apply height-based transformation
        if stack_height == 2:
            output_grid[stack[-1]] = 8  # Bottom-most pixel
        elif stack_height >= 3:
            output_grid[stack[-1]] = 8  # Bottom-most pixel
            output_grid[stack[-2]] = 8  # Second-to-bottom pixel

    return output_grid