# ce4f8723 • 012 • refine_coder

---
```python
"""
1.  Identify the largest solid rectangle of non-zero color within the input grid.
2.  Determine output dimensions: The output grid's height is one less than the identified rectangle's height, divided by two rounded down if necessary.  The output grid's width is one less than the width of the identified rectangle, divided by two.
3.  Populate the output grid: Create an output of the specified dimensions filled with 0. Overlay a rectangle of color 3 with height and width matching output dimensions divided by two, rounded down. This rectangle should be centered within the output grid.
"""

import numpy as np

def find_largest_rectangle(grid):
    """Finds the largest solid rectangle of non-zero color."""
    max_area = 0
    rect_height = 0
    rect_width = 0
    rect_color = 0

    for color in range(1, 10):  # Check colors 1-9
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r, c] == color:
                    # Expand rectangle as much as possible
                    h = 1
                    w = 1
                    while r + h < grid.shape[0] and np.all(grid[r:r+h+1, c] == color):
                        h += 1
                    h -= 1 # correct the extra 1
                    while c + w < grid.shape[1] and np.all(grid[r:r+h, c:c+w+1] == color):
                        w+=1
                    w -= 1
                    area = h * w

                    if area > max_area:
                        max_area = area
                        rect_height = h
                        rect_width = w
                        rect_color = color
    return rect_height, rect_width, rect_color

def transform(input_grid):
    input_grid = np.array(input_grid)

    # Find the largest solid rectangle
    rect_height, rect_width, _ = find_largest_rectangle(input_grid)

    # Determine output dimensions
    output_height = (rect_height ) // 2 + (rect_height %2)
    output_width = (rect_width) // 2 + (rect_width % 2)

    # Create output grid filled with 0
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Calculate dimensions of the centered rectangle (color 3)
    overlay_height = output_height // 2 + (output_height % 2) - (output_height//2==0) # prevent zero size
    overlay_width = output_width // 2 + (output_width % 2) - (output_width //2 == 0)

    # Calculate top-left corner for centering
    start_row = (output_height - overlay_height) // 2
    start_col = (output_width - overlay_width) // 2

    # Overlay the rectangle of color 3
    output_grid[start_row:start_row + overlay_height, start_col:start_col + overlay_width] = 3

    return output_grid.tolist()
```
