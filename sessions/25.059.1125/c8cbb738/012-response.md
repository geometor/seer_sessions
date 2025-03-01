# c8cbb738 • 012 • example_2 • investigate_coder

---
```python
"""
1. Identify Key Colors: Find all colors present in the input grid, excluding the most frequent color which is the background color.
2. Find Central Region: Locate a 3x3 region in the input grid centered on a blue pixel.
3. Locate Critical Pixel: Find the blue(1) pixel in the input that is adjacent to an azure(8) and a green(3).
4. Extract Subgrid: Extract the 3x3 subgrid centered at the critical pixel.
5. Output Subgrid: Return the extracted subgrid.
"""

import numpy as np

def find_critical_pixel(grid, background_color, key_colors):
    """Finds the blue pixel adjacent to both azure and green pixels."""
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r, c] == background_color:
                neighbors = [grid[r-1, c], grid[r+1, c], grid[r, c-1], grid[r, c+1]]
                if all(color in neighbors for color in key_colors):
                    return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid to the output grid based on the described rules."""
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)
    
    # Identify background color (most frequent)
    values, counts = np.unique(input_grid, return_counts=True)
    background_color = values[np.argmax(counts)]

    # Identify Key Colors
    key_colors = [color for color in values if color != background_color]
       
    # Find the critical blue pixel.
    critical_pixel = find_critical_pixel(input_grid, background_color, key_colors)

    # Extract the 3x3 subgrid.
    if critical_pixel:
      r, c = critical_pixel
      output_grid = input_grid[r-1:r+2, c-1:c+2]
    else:
      output_grid = np.zeros((3,3))

    return output_grid.tolist()
```
