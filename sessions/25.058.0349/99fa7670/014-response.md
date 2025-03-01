# 99fa7670 • 014 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Seed Pixels:** Locate all non-zero pixels within the input grid. These are the "seed" pixels.
2.  **Horizontal Expansion (Azure):** For each seed pixel that is azure (value 8), extend it horizontally to fill the entire row it occupies in the output grid.
3. **Expansion to bottom right (Gray)**: The grey pixel seems to fill the cells down and to its right.
"""

import numpy as np

def find_seed_pixels(grid):
    """Finds the coordinates of non-zero pixels in the grid."""
    seed_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel_value in enumerate(row):
            if pixel_value != 0:
                seed_pixels.append((row_index, col_index, pixel_value))
    return seed_pixels

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find seed pixels and their colors.
    seed_pixels = find_seed_pixels(input_grid)

    # Iterate through each seed pixel.
    for row, col, value in seed_pixels:
        if value == 8:  # Azure pixel
            # Horizontal expansion
            output_grid[row, :] = 8
        elif value == 5: # Gray pixel
            # expand down and right
            output_grid[row:, col:] = np.where(output_grid[row:,col:]==0,5,output_grid[row:,col:])
        
    return output_grid
```
