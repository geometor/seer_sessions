# ce9e57f2 • 016 • refine_coder

---
```python
"""
1. Identify Red Pixels: Locate all pixels with the color red (value 2) in the input grid.
2. Check for Vertical Stacking: for each column containing red, sort the red pixels by row.
3. Conditional Replacement:
    a.  If the red pixel is not at the top of the stack, replace it with azure (value 8).
    b.  Otherwise, keep it as red (value 2)
4. Output: Generate the output grid with the replaced pixels, keeping all other non-red pixels unchanged.
"""

import numpy as np

def get_red_pixels(grid):
    """
    Returns a list of (row, col) tuples representing the positions of red pixels.
    """
    red_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((row_index, col_index))
    return red_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)

    # Create a dictionary to store red pixels by column
    red_pixels_by_column = {}
    for r, c in red_pixels:
        if c not in red_pixels_by_column:
            red_pixels_by_column[c] = []
        red_pixels_by_column[c].append((r, c))

    # Iterate through the red pixels and apply replacement logic
    for c, pixels in red_pixels_by_column.items():
        #sort the pixels in the column by the row
        pixels.sort()

        #if only 1 pixel, change to azure.
        if len(pixels) == 1:
            row = pixels[0][0]
            col = pixels[0][1]
            output_grid[row][col] = 8

        #if only 1 pixel keep
        if len(pixels) > 1:
          #starting at the second pixel, replace all with azure
          for i in range(1,len(pixels)):
            row = pixels[i][0]
            col = pixels[i][1]
            output_grid[row][col] = 8

    return output_grid
```
