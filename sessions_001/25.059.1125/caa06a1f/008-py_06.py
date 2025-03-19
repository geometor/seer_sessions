"""
1.  **Locate the Green Region:** Identify the bounding box of the contiguous green (3) region in the input grid.  Record its x_start, y_start, width, and height.
2.  **Create Output Grid:** Create an output grid filled with black (0), matching the input grid's dimensions.
3.  **Generate Checkerboard:** Within the output grid, at the location identified by the green region's x_start and y_start, create a checkerboard pattern of orange (7) and magenta (6) pixels.  The checkerboard's dimensions are the same as the green region's width and height. The checkerboard starts with orange at its top-left corner (x_start, y_start), and the colors alternate in both horizontal and vertical directions.
4. **Remove other colors**: Ensure that there are no other colors from the input in the output.
"""

import numpy as np

def get_region_bounds(grid, color):
    """Finds the bounding box of a region of the specified color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Handle cases where the color isn't present
    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return {
        'x_start': int(min_x), 'x_end': int(max_x),
        'y_start': int(min_y), 'y_end': int(max_y),
        'width': int(max_x - min_x + 1),
        'height': int(max_y - min_y + 1),
    }

def transform(input_grid):
    # Create output grid filled with black, matching input dimensions.
    output_grid = np.zeros_like(input_grid)

    # Locate the Green Region
    green_region = get_region_bounds(input_grid, 3)

    if green_region is None:
        return output_grid # if no green, return the black grid

    # Generate Checkerboard within the bounds of the green region
    for y in range(green_region['height']):
        for x in range(green_region['width']):
            abs_y = y + green_region['y_start']
            abs_x = x + green_region['x_start']
            if (x + y) % 2 == 0:
                output_grid[abs_y, abs_x] = 7  # Orange
            else:
                output_grid[abs_y, abs_x] = 6  # Magenta

    return output_grid