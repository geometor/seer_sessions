"""
1.  **Initialization:** The input is an 8x8 grid of colored pixels.
2.  **Identify Trigger Column:** The fourth column (index 3) is identified as the "trigger column".
3. **Identify Target Column:** The fifth column (index 4) is the target column.
4.  **Conditional Color Change:** *All* pixels within the trigger column (index 3) are changed to match the color of the pixel directly to their right, in column 4 (index 4) *if* they are a specific "trigger" color. The trigger color appears to be different in different grids, but consistently applies to all rows within a given grid, except in Example 3, where pixels in column 3 change to color 0, regardless of color in column 4.
5.  **Preservation:** All other pixels retain their original color and position.
6.  **Output Production:** The output is the modified 8x8 grid.
"""

import numpy as np

def get_trigger_colors(input_grid):
    # Helper function to determine the trigger color(s) for a given input grid.
    # Checks the first changed pixel to infer the trigger color.  Handles Example 3's behavior.
    changes = []
    for r in range(input_grid.shape[0]):
        if input_grid[r, 3] != 0:
            changes.append(input_grid[r,3])

    if all(c == changes[0] for c in changes):
        return [changes[0]]     
    else:
        # handles example 3 behavior
        trigger_colors = []
        for r in range(input_grid.shape[0]):
           if input_grid[r,3] not in trigger_colors:
               trigger_colors.append(input_grid[r,3])
        return trigger_colors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])
    trigger_colors = get_trigger_colors(input_grid)

    # change output pixels 
    for i in range(rows):
        # find the trigger color, if more than one, use color at trigger column
        if len(trigger_colors) > 1:
            trigger_color = output_grid[i,3]
        else:
            trigger_color = trigger_colors[0]
       
        if output_grid[i, 3] == trigger_color:  # Check if the pixel matches the trigger color
                # handles example 3 behavior
                if 0 in trigger_colors and len(trigger_colors) > 1:
                    output_grid[i,3] = 0
                else:
                    output_grid[i, 3] = output_grid[i, 4]  # change color

    return output_grid