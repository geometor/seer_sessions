# cbded52d • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves selectively shifting green and possibly orange pixels down *one* position vertically within their respective columns, while leaving all other pixels unaltered.
"""

import numpy as np

def find_columns_with_colors(grid, colors):
    """Finds columns containing specified colors."""
    cols = set()
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel in colors:
                cols.add(c)
    return list(cols)

def shift_pixel_down(grid, col, color):
    """Shifts the first instance of specified color down by one position in a column."""
    rows, cols = grid.shape
    color_positions = []

    #find all instances of color in col
    for r in range(rows):
      if grid[r,col] == color:
        color_positions.append(r)

    if len(color_positions) > 0:
        first_color_row = color_positions[0] #only process first instance of a given color

        if first_color_row + 1 < rows:  # Check if we can shift down
            # Swap the pixel with the one below it
            #print(grid[first_color_row + 1, col])
            target_color = grid[first_color_row + 1, col]
            grid[first_color_row + 1, col] = color
            grid[first_color_row, col] = target_color

    return grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    # Find columns of interest (containing 3 or 7)
    target_colors = [3, 7]
    columns_of_interest = find_columns_with_colors(output_grid, target_colors)
    #print("cols of interest",columns_of_interest)

    #process all columns
    for col in columns_of_interest:
      for color in target_colors: #need to test each color down shift
        #move first instance of color down one pixel
        output_grid = shift_pixel_down(output_grid,col,color)

    return output_grid
```
