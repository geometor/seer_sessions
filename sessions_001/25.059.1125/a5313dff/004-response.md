# a5313dff • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the hollow red square:** Locate the contiguous block of red pixels (value 2) that forms a hollow square.
2.  **Define the interior:** Determine the boundaries of the empty space enclosed by the red square.
3. **Fill with blue** Change all of the pixels inside that boundary to blue(value 1).
4.  **Preserve the rest:** All other pixels remain unchanged.
"""

import numpy as np

def find_hollow_square(grid, color):
    rows, cols = grid.shape
    top_left = None
    bottom_right = None

    # Find top-left and bottom-right corners of the outer square
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == color:
                if top_left is None:
                    top_left = (i, j)
                bottom_right = (i, j)

    if top_left is None:  # No square found
        return None, None

    return top_left, bottom_right

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Find the hollow red square (color 2)
    top_left, bottom_right = find_hollow_square(input_grid, 2)

    if top_left and bottom_right:
      # Fill in the interior with blue (color 1)
      for i in range(top_left[0] + 1, bottom_right[0]):
          for j in range(top_left[1] + 1, bottom_right[1]):
              output_grid[i, j] = 1

    return output_grid
```
