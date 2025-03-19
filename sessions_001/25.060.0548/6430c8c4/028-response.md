# 6430c8c4 • 028 • refine_coder

---
```python
"""
1.  **Identify Shapes:** For each input grid, identify all distinct shapes. A shape is a group of connected pixels of the same color, excluding the background (black).
2.  **Color Mapping:** For each shape identified, determine its color in the input grid.
3.  **Transform Color:** Transform the input color to its corresponding output color using the color mapping.
    *   Orange (7) becomes Green (3).
    *   Magenta (6) becomes Blue (1).
    *  Red (2) becomes Cyan (8).
4. **Preserve Geometry:** The output grid retains the exact same shapes, sizes, and positions as the input grid. Only the colors of the shapes change according to the mapping.
"""

import numpy as np

def find_shapes(grid):
    visited = set()
    shapes = []

    def dfs(r, c, color, shape_coords):
        if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
            return
        visited.add((r, c))
        shape_coords.append((r, c))
        dfs(r + 1, c, color, shape_coords)
        dfs(r - 1, c, color, shape_coords)
        dfs(r, c + 1, color, shape_coords)
        dfs(r, c - 1, color, shape_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0:  # Ignore background
                    shape_coords = []
                    dfs(r, c, color, shape_coords)
                    shapes.append((color, shape_coords))
    return shapes

def transform_color(input_color):
    color_map = {
        7: 3,  # Orange to Green
        6: 1,  # Magenta to Blue
        2: 8   # Red to Cyan
    }
    return color_map.get(input_color, input_color) # returns input_color if not in map


def transform(input_grid):
    # initialize output_grid with the same dimensions and background color
    output_grid = np.zeros_like(input_grid)

    # identify shapes in the input grid
    input_shapes = find_shapes(input_grid)
    
    # iterate through the identified shapes and transform the color while keeping coordinates the same
    for color, coords in input_shapes:
        new_color = transform_color(color) # transform the color
        for r, c in coords:
            output_grid[r, c] = new_color  # place the new color

    return output_grid
```
