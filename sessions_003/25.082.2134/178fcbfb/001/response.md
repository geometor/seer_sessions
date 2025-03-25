```python
"""
1.  **Identify Target Color:** It appears that the last color from top to bottom in the original grid is repeated downwards on its original location.
2.  **Replicate Down:** Make copies of the column of target color for all rows.
3.  **Identify Other Colors:** Find all other colors present in the input grid.
4.  **Fill Rows:** For each of the other colors, fill a single, complete row with that color. The chosen row index should be equal to the row index where each 'other color' first appears.
"""

import numpy as np

def get_colored_pixels(grid):
    """Finds coordinates and colors of non-black pixels."""
    pixels = []
    for r_idx, row in enumerate(grid):
        for c_idx, color in enumerate(row):
            if color != 0:
                pixels.append(((r_idx, c_idx), color))
    return pixels


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # get the colored pixels
    colored_pixels = get_colored_pixels(input_grid)

    # Identify Target Color (last color)
    target_pixels = []
    if colored_pixels:
        target_pixels = [colored_pixels[-1]]

        #find same color in the array
        last_color = target_pixels[0][1]
        for pixel in reversed(colored_pixels):
            if pixel[1] == last_color:
                target_pixels.append(pixel)
            else:
                break


    # Replicate target color down
    for ((r, c), color) in target_pixels:
        for i in range(height):
            output_grid[i, c] = color
    
    # Identify Other Colors, exclude target_color
    other_colors = []
    for ((r, c), color) in colored_pixels:
        is_target = False
        for ((tr, tc), tcolor) in target_pixels:
          if color == tcolor:
            is_target = True
            break
        if not is_target:
          other_colors.append(((r,c), color))

    # Fill Rows with Other Colors
    for ((r, c), color) in other_colors:
        output_grid[r, :] = color

    return output_grid.tolist()
```