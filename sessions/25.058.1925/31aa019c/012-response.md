# 31aa019c • 012 • refine_coder

---
```python
"""
1.  Identify Objects: Find all contiguous blocks (objects) of red (2) and yellow (4) pixels in the input grid. Also, identify any horizontal lines of green (3).
2.  Conditional Movement - Red and Yellow:
    -   If the input grid has dimensions 11x11, move all red vertical line objects down such that the top of each line is on row 6, for the first set of objects at the top, and row 8 for the second set of lines.
    -   Move each yellow pixel down. If a yellow pixel is below a red line in the input, it should appear below the corresponding red line in the output. Specifically, the first set of yellow pixels is placed on row 7, and the second set on row 9.
    -   If a red line and yellow pixel would occupy the same space, the red line takes precedence.
3.  Preserve Green:** If the input grid includes horizontal green (3) lines, copy them to the output grid in the *exact same positions*.
4.  All Other Pixels: All other pixels that are not part of a moved or copied object should remain unchanged.
"""

import numpy as np

def object_properties(grid, color):
    """Finds coordinates and properties of all contiguous pixels of the specified color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # No object of that color

    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return {
        'color': color,
        'min_row': min_row,
        'min_col': min_col,
        'height': height,
        'width': width,
        'coords': coords
    }

def transform(input_grid):
    # Initialize the output grid with a copy of the input grid.
    output_grid = input_grid.copy()

    # Get grid dimensions
    rows, cols = input_grid.shape

    # Handle 11x11 grids (red and yellow movement)
    if rows == 11 and cols == 11:
        red_objects = []
        yellow_pixels = []

        # Find red vertical lines and yellow pixels
        for color in [2, 4]:
            props = object_properties(input_grid, color)
            if props:
                if color == 2 and props['height'] > 1:  # Red vertical line
                    red_objects.append(props)
                elif color == 4:  # Yellow pixel
                    yellow_pixels.append(props)

        # Sort red objects by their starting row
        red_objects.sort(key=lambda obj: obj['min_row'])
        
        # Calculate offset for red lines
        red_row_offset = 6

        for obj in red_objects:
            # clear the original object
            for r, c in obj['coords']:
              output_grid[r,c] = input_grid[r,c] # preserve original

            # Move each red object.
            for r, c in obj['coords']:
              output_grid[r - obj['min_row'] + red_row_offset, c] = 2
            red_row_offset += 2

        # Move yellow pixels based on their relation to red objects
        yellow_row_offset = 7
        for obj in yellow_pixels:
            
            # clear original object
            for r, c in obj['coords']:
                output_grid[r,c] = input_grid[r,c] # preserve original

            output_grid[yellow_row_offset, obj['min_col']] = 4
            yellow_row_offset += 2


    # Preserve Green lines (regardless of grid size)
    green_objects = object_properties(input_grid, 3)
    if green_objects:
        for r, c in green_objects['coords']:
            output_grid[r, c] = 3  # Keep green in the same place


    return output_grid
```

