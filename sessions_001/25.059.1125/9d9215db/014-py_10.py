"""
1.  **Object Identification**: The grid contains blue, yellow, green, and white pixels.

2.  **Green Pixel Movement:**
    *   Each green pixel moves one step vertically *towards* the center of the grid.
    *   If a green pixel is above the horizontal center line (calculated as `grid_height // 2`), it moves one step down.
    *   If a green pixel is below the horizontal center line, it moves one step up.
    *   If a green pixel is *on* the horizontal center line, it remains in place.

3.  **Yellow Pixel Mirroring:** Each yellow pixel is mirrored across the horizontal center line. The new vertical (y) position is calculated as `new_y = (grid_height - 1) - old_y`. The original yellow pixel is removed.

4.  **Blue Pixel Mirroring and Expansion:**
    *   Each blue pixel is first mirrored across the horizontal center line, calculated as `new_y = (grid_height - 1) - old_y`.
    * The original blue pixel is removed.
    *   The mirrored blue pixel then expands horizontally, filling all cells from x=3 to x=15 (inclusive) with blue.

5.  **Order of Transformations**: The order of operations is crucial for correct results, to prevent color changes impacting subsequent logic:
    a. Green Pixel Movement
    b. Yellow Pixel Mirroring
    c. Blue Pixel Mirroring and Expansion

6. **White Pixels**: White pixels remain unchanged throughout the entire process.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    grid_height = output_grid.shape[0]
    center_y = grid_height // 2

    # Create a temporary grid to store intermediate changes
    temp_grid = np.copy(input_grid)

    # Green Pixel Movement
    for y in range(grid_height):
        for x in range(grid_width):
            if input_grid[y, x] == 3:
                temp_grid[y,x] = 0
                if y < center_y:
                    temp_grid[y + 1, x] = 3
                elif y > center_y:
                    temp_grid[y - 1, x] = 3
    
    # copy temp to output
    output_grid = np.copy(temp_grid)

    # Yellow Pixel Mirroring
    for y in range(grid_height):
        for x in range(grid_width):
            if temp_grid[y, x] == 4:
                new_y = (grid_height - 1) - y
                output_grid[y,x] = 0  # Clear original
                output_grid[new_y, x] = 4

    # copy output to temp for next operation
    temp_grid = np.copy(output_grid)
                
    # Blue Pixel Mirroring and Expansion
    for y in range(grid_height):
        for x in range(grid_width):
            if temp_grid[y, x] == 1:
                new_y = (grid_height - 1) - y
                output_grid[y,x]=0 # Clear original
                for i in range(3, 16):  # Expand horizontally
                    output_grid[new_y, i] = 1

    return output_grid