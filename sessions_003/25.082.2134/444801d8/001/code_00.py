"""
1.  **Identify Blue Objects:** Find all horizontal lines composed entirely of blue (1) pixels.

2.  **Identify Isolated Pixels:** Within each blue object, check for the presence of single pixels of any colors other than blue (red (2), green (3), magenta (6), azure (8)).

3. **Determine location of Isolated Pixels**: Check if the isolated pixel is present within the upper horizontal blue object or the lower horizontal blue object.

4.  **Replace Colors:**
    *   If a isolated pixel is present in the upper blue object, replace the isolated pixel's color with the color of the isolated pixel, and replace any immediately adjacent blue pixels with the color of the isolated pixel.
    *    If a isolated pixel is present in the lower blue object, replace the isolated pixel's color with the color of the isolated pixel, and replace any immediately adjacent blue pixels with the color of the isolated pixel.

5.  **Preserve other parts:** Leave all other pixels (including the blue (1) pixels *not* directly adjacent to the replaced pixels) unchanged. The "frame" of 0s remains.
"""

import numpy as np

def find_horizontal_blue_objects(grid):
    blue_objects = []
    for i, row in enumerate(grid):
        start = -1
        for j, pixel in enumerate(row):
            if pixel == 1:
                if start == -1:
                    start = j
            elif start != -1:
                blue_objects.append((i, start, j - 1))
                start = -1
        if start != -1:
            blue_objects.append((i, start, len(row) - 1))
    return blue_objects

def find_isolated_pixels(grid, blue_object):
    row, start, end = blue_object
    isolated_pixels = []
    for j in range(start, end + 1):
        if grid[row, j] != 1:
            isolated_pixels.append((row, j))
    return isolated_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)

    # Find horizontal blue objects
    blue_objects = find_horizontal_blue_objects(grid)

    # Process each blue object
    for blue_object in blue_objects:
        row, start, end = blue_object
        
        # Find isolated pixels within the blue object
        isolated_pixels = find_isolated_pixels(grid, blue_object)

        # Replace colors based on isolated pixels
        for isolated_row, isolated_col in isolated_pixels:
            isolated_color = grid[isolated_row, isolated_col]
            output_grid[isolated_row, isolated_col] = isolated_color
            
            # Replace adjacent blue pixels to the left.
            for j in range(isolated_col - 1, start -1, -1):
                if grid[isolated_row, j] == 1:
                    output_grid[isolated_row, j] = isolated_color
                else:
                    break
            
            #Replace adjacent blue pixels to the right
            for j in range(isolated_col + 1, end + 1):
                if grid[isolated_row, j] == 1:
                    output_grid[isolated_row,j] = isolated_color
                else:
                    break

    return output_grid.tolist()