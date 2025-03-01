# 72322fa7 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Key Colors:** Focus on pixels with colors 1 (blue), 3 (green), 6 (magenta), and 8 (azure).
2.  **Blue (1) Replication:**
    *   If a single blue (1) pixel is present in row, create a mirror image of this single pixel in the same row.
    *   If two blue (1) pixels are present, check if they are mirrored, maintain mirrored pixels in the same row.
3.  **Green (3) Preservation:** Green (3) pixels remain unchanged in their original positions.
4.  **Magenta (6) and Azure (8) Transformation:**
    *   All Magenta (6) pixels become Azure (8).
    *   Azure (8) pixel creates a mirror of itself.
    *    If a row has transformed Azure pixels, copy them in the row of the original Azure pixels.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    return np.argwhere(grid == color)

def mirror_pixel(grid, coord):
    """Mirrors a single pixel across a vertical axis derived from the input grid's overall shape."""
    rows, cols = grid.shape
    x, y = coord
    
    # central column.
    mirror_y = cols - 1 - y

    return (x, mirror_y)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # 1. Blue (1) Replication
    blue_pixels = find_pixels(input_grid, 1)
    for x, y in blue_pixels:
      mirrored_coord = mirror_pixel(output_grid,(x,y))
      output_grid[mirrored_coord] = 1

    # 2. Green (3) Preservation (no change needed)

    # 3. Magenta (6) and Azure (8) Transformation
    magenta_pixels = find_pixels(input_grid, 6)
    azure_pixels = find_pixels(input_grid,8)
    
    #store original positions before change
    original_azure_rows = {x for x, _ in azure_pixels}

    for x, y in magenta_pixels:
        output_grid[x, y] = 8  # Magenta becomes Azure
        mirrored_coord = mirror_pixel(output_grid,(x,y))
        output_grid[mirrored_coord] = 8

    transformed_azure_pixels = find_pixels(output_grid,8)

    transformed_azure_rows = []

    for x,_ in transformed_azure_pixels:
        transformed_azure_rows.append(x)
    
    #filter only to new azure rows
    new_azure_rows = list(set(transformed_azure_rows) - original_azure_rows)
    
    if (len(new_azure_rows) > 0):
        for row in original_azure_rows:
            for new_row in new_azure_rows:
                for _,y in transformed_azure_pixels:
                     if output_grid[new_row,y] == 8:
                        output_grid[row,y] = 8


    for x,y in azure_pixels:
        mirrored_coord = mirror_pixel(output_grid,(x,y))
        output_grid[mirrored_coord] = 8
    

    return output_grid
```
