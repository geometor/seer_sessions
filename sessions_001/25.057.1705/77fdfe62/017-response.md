# 77fdfe62 • 017 • refine_coder

---
```python
"""
1.  Identify Colored Pixels: Find all pixels in the input grid that are not color 0 (white/background) and are not color 5 (grey).
2.  Create 2x2 Blocks: For *each* of these colored pixels, create a 2x2 block of pixels of the same color in the output grid. The top-left corner of each 2x2 block corresponds to the row and column divided by two (using integer division - rounding down): `new_row = row // 2 * 2` and `new_col = col // 2 * 2`.
3. Preserve 1 and 0 pixels: Pixels that are color 1 and color 0 (white) and remain unchanged.
4. Treat 5 as a colored pixel: repeat step 2, include pixels that are color 5 (grey)
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height = (input_height // 2 + (input_height % 2)) * 2
    output_width = (input_width // 2 + (input_width % 2)) * 2
    
    #adjust output size for the edge cases where colored objects are at the edges
    max_colored_row = 0
    max_colored_col = 0
    for r in range(input_height):
        for c in range(input_width):
             if input_grid[r,c] != 0 and input_grid[r,c] != 1:
                max_colored_row = max(max_colored_row, r)
                max_colored_col = max(max_colored_col, c)
    output_height = max(output_height, (max_colored_row // 2 + 1) * 2)
    output_width = max(output_width, (max_colored_col // 2 + 1) * 2)
    
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy color 1 and 0 pixels to the output grid
    for r in range(input_height):
      for c in range(input_width):
          if input_grid[r,c] == 0 or input_grid[r,c] == 1:
            if r < output_height and c < output_width: #stay in bounds
                output_grid[r,c] = input_grid[r,c]

    # change output pixels
    for r in range(input_height):
        for c in range(input_width):
            color = input_grid[r, c]
            if color != 0 and color != 1:  # Process all non-background, and non-1 pixels
                new_row = (r // 2) * 2
                new_col = (c // 2) * 2
                # Create 2x2 block
                if new_row < output_height and new_col < output_width: #stay in bounds
                    output_grid[new_row:new_row+2, new_col:new_col+2] = color

    return output_grid
```
