# f8b3ba0a • 008 • refine_coder

---
```python
"""
1.  **Identify Target Colors:** Find the presence of yellow (4), red (2), and green (3) within the input grid.
2.  **Determine Output Height:** The output grid's height is equal to the number of target colors found in the input grid.
3.  **Determine Output Width:** If *any* row in the input grid contains only one non-zero color and any of the target colors, then the width is the same with the input. Otherwise the output width is 1.
4. **Populate Output:** create rows of the target color and size based on the determined output shape.

"""

import numpy as np

def get_target_colors(grid):
    """
    Finds the unique target colors present in the grid.
    """
    target_colors = [4, 2, 3]  # Yellow, Red, Green
    found_colors = set()
    for row in grid:
        for cell in row:
            if cell in target_colors:
                found_colors.add(cell)
    return sorted(list(found_colors))

def determine_output_width(grid, target_colors):
   rows, cols = len(grid), len(grid[0])
   for r in range(rows):
       row_colors = set()
       for cell in grid[r]:
           if cell != 0:
               row_colors.add(cell)
       if len(row_colors) == 1 and len(row_colors.intersection(target_colors)) > 0:
           return cols
   return 1

def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    input_grid_np = np.array(input_grid)
    target_colors = get_target_colors(input_grid_np)
    output_height = len(target_colors)
    output_width = determine_output_width(input_grid_np, target_colors)

    output_grid = np.zeros((output_height, output_width), dtype=int)
   
    for i, color in enumerate(target_colors):
      output_grid[i, :] = color

    return output_grid.tolist()
```
