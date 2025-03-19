# bda2d7a6 • 006 • refine_coder

---
```python
"""
1. Identify Layers: Observe and distinguish the different colored regions in the input grid. These typically include an outer border (color varies), an inner region (color varies), and a central white square.
2. Remove Center: Eliminate the central white square (color 0).
3. Shift Inwards: Expand the inner region's color to fill the area previously occupied by the central white square.
4. Blank Perimeter: Set all pixels on the grid's outermost border to white (color 0).
"""

import numpy as np

def get_inner_region_color(grid):
    # Find the color of the inner region by checking neighbors of the white center
    center_coords = np.argwhere(grid == 0)
    if len(center_coords) == 0:
      return None

    # Consider neighbors of the first center pixel
    center_row, center_col = center_coords[0]
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            row = center_row + dr
            col = center_col + dc
            if 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]:
                neighbors.append(grid[row, col])

    # Filter and return the neighbor color
    inner_colors = [c for c in neighbors if c !=0]
    if (len(inner_colors) > 0):
        return inner_colors[0]
    else:
      return None

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)

    # Remove Center
    center_coords = np.argwhere(output_grid == 0)
    
    # Shift Inwards - Find the color of the adjacent layer to the center
    inner_color = get_inner_region_color(input_grid)
        
    # Shift inwards - move inner color
    for coord in center_coords:
      if inner_color is not None:
        output_grid[coord[0], coord[1]] = inner_color

    # Blank the perimeter.
    rows, cols = output_grid.shape
    for i in range(rows):
        for j in range(cols):
          if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                output_grid[i,j] = 0
          

    return output_grid
```
