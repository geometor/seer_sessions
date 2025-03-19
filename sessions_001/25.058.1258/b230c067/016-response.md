# b230c067 • 016 • refine_coder

---
```python
"""
1.  **Identify the Azure Shape:** Locate the contiguous region of azure (8) pixels in the input grid. This forms the "azure shape".
2.  **Recolor the Azure Shape:** Change all pixels within the identified azure shape to blue (1).
3.  **Identify the outline:** Find the white (0) pixels adjacent to the *original* location of the azure shape.
4.  **Recolor Outline:** Change all identified white outline pixels to red (2).
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    return coords

def get_outline(grid, object_coords):
    # finds the outline of the object - specifically background cells
    outline_coords = []
    rows, cols = grid.shape

    for r, c in object_coords:
        # Check neighbors (up, down, left, right)
        neighbors = []
        if r > 0:
            neighbors.append((r-1,c))
        if r < rows-1:
            neighbors.append((r+1, c))
        if c > 0:
            neighbors.append((r,c-1))
        if c < cols-1:
            neighbors.append((r, c+1))

        for nr, nc in neighbors:
            if grid[nr, nc] == 0: # Check for background color
                outline_coords.append((nr,nc))

    return outline_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Identify the Azure Shape
    azure_coords = find_object(input_grid, 8)

    # Handle the case where no azure pixels are found.
    if azure_coords is None:
      return output_grid

    # 2. Recolor the Azure Shape
    for r, c in azure_coords:
        output_grid[r, c] = 1

    # 3. Identify the outline (original location, background cells)
    outline = get_outline(input_grid, azure_coords)

    # 4. Recolor Outline
    for r, c in outline:
        output_grid[r, c] = 2

    return output_grid
```
