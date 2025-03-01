# 46442a0e • 017 • refine_coder

---
```python
"""
1.  **Identify the Central Object:** Locate the contiguous region of pixels with color 4 (yellow) within the input grid. This is the central object.

2.  **Determine Output Dimensions:** Create a new output grid that is twice the width and twice the height of the input grid.

3.  **Expand Central Object:** In the output grid, expand the central object (color 4) in the input grid to fill at least 2x2 at center of new grid.

4.  **Identify border colors:** Note values of non-yellow color, and use this with color 6 for borders.

5. **Create border:** Create a border around center object. Alternate colors 6 and the other color from the input.

6.  **Fill Output:** The final output grid is created by expanding center object, and filling borders as described above.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels matching the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    return coords

def transform(input_grid):
    # Determine output dimensions (twice the input)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Identify the central object (color 4)
    object_coords = find_object(input_grid, 4)

    # Determine border colors
    border_colors = [c for c in np.unique(input_grid) if c != 4]
    if len(border_colors) > 1:
        # If there's 9(maroon), use it with 6(magenta); else, just use 6.
        border_color = border_colors[0] if border_colors[0]!=0 else border_colors[1]
    else:
        border_color = border_colors[0]

    # Expand and place Central object in output
    if object_coords is not None:
        min_row = np.min(object_coords[:, 0])
        min_col = np.min(object_coords[:, 1])

    # output_grid[min_row*2:min_row*2+2, min_col*2:min_col*2+2] = 4
    for r in range(rows * 2):
       for c in range(cols * 2):
          if (rows%2 == 1):
            if r >= rows - rows//2 -1 and r <= rows + rows//2  and c >= cols - cols//2 -1 and c <= cols+cols//2:
              output_grid[r,c] = 4
          else:
            if r >= rows - rows//2 -1 and r <= rows + rows//2 and c >= cols - cols//2 -1 and c <= cols+cols//2:
              output_grid[r,c] = 4

    # Fill border with alternating colors, starting from top-left
    for r in range(rows * 2):
        for c in range(cols * 2):
            if output_grid[r,c] != 4:  # Only fill non-object cells
              if (r+c) % 2 == 0:
                    output_grid[r, c] = 6
              else:
                    output_grid[r,c] = border_color

    return output_grid
```
