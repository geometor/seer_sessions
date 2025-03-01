# 0a938d79 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to fill the output grid with a repeating, alternating pattern of red (2) and azure (8) pixels, starting from the position of the original red pixel in the input grid. The pattern extends across each row.
"""

import numpy as np

def find_first_non_zero_pixel_positions(grid):
    """Finds the positions of the non-zero pixels and their corresponding colors."""
    non_zero_positions = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                if grid[r,c] not in non_zero_positions:
                  non_zero_positions[grid[r,c]] = (r,c)

    return non_zero_positions


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Find non-zero pixel positions and color
    non_zero_pixels = find_first_non_zero_pixel_positions(input_grid)
    if not non_zero_pixels:
        return output_grid

    # Get starting position from first non-zero element
    first_entry = list(non_zero_pixels.keys())
    red_value = first_entry[0]
    red_start_col = non_zero_pixels[first_entry[0]][1]


    try:
       azure_value = first_entry[1]
    except:
       azure_value = red_value


    # Fill the output grid with the alternating pattern
    for r in range(rows):
        current_col = red_start_col
        color_index = 0
        colors = [red_value, azure_value]
        for c in range(cols):

          output_grid[r,c] = colors[color_index % 2]
          color_index+=1


    return output_grid
```
