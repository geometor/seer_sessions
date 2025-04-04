# dc0a314f • 010 • example_2 • investigate_coder

---
```python
"""
1. **Identify the Region of Interest:** Locate the large central region of primarily orange (7) and red (2) pixels. The output only contains colors found inside of this section, ignoring color 3 (green).
2. **Define Boundaries:** The section seems to be taken from the bottom left of the green area.
3. **Extract the region.** Extract a 5x5 subgrid from the identified region of interest in the input grid. The output appears to be a cutout of part of the larger shape in the center of the input. It is a perfect square, so a good first guess will be that it is a direct cutout.
4. **Output Creation**: The selected subgrid of 5x5 is then the output.
"""

import numpy as np

def find_object_by_color(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Convert input_grid to a numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the bounding box of the green region (color 3).
    green_bbox = find_object_by_color(input_grid, 3)
    
    #initialize to empty
    output_grid = np.empty((0, 0), dtype=int)

    if green_bbox:
        # Determine the starting point for extraction.
        # it is at the bottom left of this region
        start_row = green_bbox[1][0] 
        start_col = green_bbox[1][1]

        # Extract the 5x5 region.
        output_grid = input_grid[start_row : start_row + 5, start_col : start_col + 5]

    return output_grid.tolist()
```
