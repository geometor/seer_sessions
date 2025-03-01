# 1c786137 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation extracts a simplified, lower-resolution representation of the input grid, 
retaining only colors 0 (white), 2 (red), 3 (green), and 5 (gray), while preserving 
the relative spatial relationships between the colored regions. It essentially "zooms out" 
and filters the input data.
"""

import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def get_center(bbox):
    if bbox is None:
      return None
    min_row, max_row, min_col, max_col = bbox
    return (min_row + max_row) // 2, (min_col + max_col) // 2
    

def transform(input_grid):
    """
    Transforms the input grid to a smaller output grid, keeping only
    colors 0, 2, 3, and 5, and preserving relative positions.
    """
    input_height, input_width = input_grid.shape
    output_height, output_width = 8, 10  # Determined from example output size
    output_grid = np.zeros((output_height, output_width), dtype=int)

    colors_to_keep = [0, 2, 3, 5]
    
    color_centers = {}

    # calculate the approximate centers for each of the colors of interest
    for color in colors_to_keep:
        bbox = get_bounding_box(input_grid, color)
        center = get_center(bbox)
        color_centers[color] = center

    # scale down to find the nearest output coordinate
    for color, center in color_centers.items():
      if center is not None:
        in_y, in_x = center
        out_x = int(in_x * output_width / input_width)
        out_y = int(in_y * output_height / input_height)

        # set that coordinate to the color
        output_grid[out_y, out_x] = color

        # get neighbors of this color in the input grid
        neighbors = []
        for dx in [-1,0,1]:
          for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
              continue

            nx = in_x + dx
            ny = in_y + dy

            if 0 <= nx < input_width and 0 <= ny < input_height:
              if input_grid[ny, nx] == color:
                # map input neighbor coordinate to output coordinate
                out_nx = int(nx * output_width / input_width)
                out_ny = int(ny * output_height / input_height)

                if 0 <= out_nx < output_width and 0 <= out_ny < output_height:
                  # add the neighbor color in the output grid if it's within bounds
                  output_grid[out_ny, out_nx] = color

    return output_grid
```
