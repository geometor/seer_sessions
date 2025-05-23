"""
1.  **Green Pixel Movement:** Every green pixel (value 3) moves one step vertically *towards* the center of the grid.
    *   If a green pixel is above the horizontal center line, it moves one step down.
    *   If a green pixel is below the horizontal center line, it moves one step up.
    * If the green pixel is on the horizontal center line, it remains.

2.  **Yellow Pixel Mirroring:** Every yellow pixel (value 4) is mirrored across the horizontal center line of the grid. The new vertical (y) position is calculated as `new_y = (grid_height - 1) - old_y`.

3.  **Blue Pixel Mirroring and Expansion:** Every blue pixel (value 1) is:
    *   First mirrored across the horizontal center line, using the same formula as the yellow pixels: `new_y = (grid_height - 1) - old_y`.
    *   Then, the mirrored blue pixel is expanded horizontally, filling all cells from x=3 to x=15 (inclusive) with the blue color.

4. **Order of operations**: The order of changes is important. Green moves. Yellow mirrors. Blue mirrors and expands.

5.  All other pixels remain unchanged. Specifically, white pixels stay white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid_height = output_grid.shape[0]
    grid_width = output_grid.shape[1]
    center_y = grid_height // 2

    # Green Pixel Movement
    for y in range(grid_height):
        for x in range(grid_width):
            if input_grid[y, x] == 3:
                output_grid[y,x] = 0 # clear original
                if y < center_y:
                    output_grid[y + 1, x] = 3
                elif y > center_y:
                    output_grid[y - 1, x] = 3

    # Yellow Pixel Mirroring
    for y in range(grid_height):
        for x in range(grid_width):
            if input_grid[y, x] == 4:
                new_y = (grid_height - 1) - y
                output_grid[y,x] = 0  # clear original
                output_grid[new_y, x] = 4


    # Blue Pixel Mirroring and Expansion
    for y in range(grid_height):
        for x in range(grid_width):
            if input_grid[y, x] == 1:
                new_y = (grid_height - 1) - y
                output_grid[y,x]=0 # clear original
                output_grid[new_y, x] = 1
                for i in range(3, 16):  # expand
                    output_grid[new_y, i] = 1

    return output_grid