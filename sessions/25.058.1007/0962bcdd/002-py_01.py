"""
1.  **Identify Crosses:** Locate all "cross" shapes in the input grid. A cross is defined as a central pixel and four adjacent pixels (up, down, left, right) of a different color.

2.  **Expand Crosses:** For each identified cross:
    *   Expand the center color into a 2x2 block of the same color, overwriting any previous values in those positions.
    *   Extend each of the four "arms" of the cross outward by one pixel in each direction, and connected at the corner, with the color of the "arm"
    * Connect the arms with a third color.

3. Replicate to fill the space between the input objects.
"""

import numpy as np

def find_crosses(grid):
    """Finds 'cross' shapes in the grid."""
    crosses = []
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            center = grid[r, c]
            arms = [grid[r-1, c], grid[r+1, c], grid[r, c-1], grid[r, c+1]]
            if all(arm != 0 and arm != center for arm in arms):
                # Check to make sure all are same arm color
                if all(arm_pixel == arms[0] for arm_pixel in arms):
                    crosses.append(((r, c), center, arms[0]))
    return crosses

def transform(input_grid):
    """Transforms the input grid according to the cross expansion rule."""
    output_grid = np.zeros_like(input_grid)
    crosses = find_crosses(input_grid)

    for (center_r, center_c), center_color, arm_color in crosses:
        # Expand center into 2x2 block
        output_grid[center_r-1:center_r+1, center_c-1:center_c+1] = center_color

        # define the corner color
        corner_color = 0
        if center_color != 2 and arm_color != 2:
            corner_color = 2
        elif center_color != 6 and arm_color != 6:
            corner_color = 6
        else:
           corner_color = 7


        # Extend arms and set corners, also handles adjacent plus replication
        # Up
        output_grid[center_r - 2, center_c] = arm_color
        output_grid[center_r - 2, center_c - 1] = corner_color
        output_grid[center_r - 2, center_c + 1] = corner_color

        # Down
        output_grid[center_r + 1, center_c] = arm_color
        output_grid[center_r + 1, center_c - 1] = corner_color
        output_grid[center_r + 1, center_c + 1] = corner_color
        # Left
        output_grid[center_r, center_c - 2] = arm_color
        output_grid[center_r - 1, center_c - 2] = corner_color
        output_grid[center_r + 1, center_c - 2] = corner_color

        # Right
        output_grid[center_r, center_c + 1] = arm_color
        output_grid[center_r - 1, center_c + 1] = corner_color
        output_grid[center_r + 1, center_c + 1] = corner_color


    return output_grid