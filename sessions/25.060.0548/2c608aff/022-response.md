# 2c608aff • 022 • example_4 • investigate_coder

---
```python
"""
The transformation identifies diagonally adjacent yellow (4) pixels in the input grid and connects them by changing the intervening blue (1) pixels to yellow (4). The gray (5) rectangle and other non-connected yellow pixels remain unchanged.
"""

import numpy as np

def get_yellow_pixels(grid):
    # returns a list of coordinates of all yellow pixels
    yellow_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 4:
                yellow_pixels.append((row_index, col_index))
    return yellow_pixels
    
def are_diagonally_adjacent(pixel1, pixel2):
    # check if two pixels are diagonally adjacent
    row_diff = abs(pixel1[0] - pixel2[0])
    col_diff = abs(pixel1[1] - pixel2[1])
    return row_diff == 1 and col_diff == 1

def transform(input_grid):
    """Transforms the input grid by connecting diagonally adjacent yellow pixels."""
    output_grid = np.copy(input_grid)
    yellow_pixels = get_yellow_pixels(input_grid)

    # Iterate through all pairs of yellow pixels
    for i in range(len(yellow_pixels)):
        for j in range(i + 1, len(yellow_pixels)):
            pixel1 = yellow_pixels[i]
            pixel2 = yellow_pixels[j]

            # Check for diagonal adjacency
            if are_diagonally_adjacent(pixel1, pixel2):
                # change the color of the intermediate pixel to connect them
                output_grid[min(pixel1[0],pixel2[0]):max(pixel1[0],pixel2[0])+1, min(pixel1[1],pixel2[1]):max(pixel1[1],pixel2[1])+1] = 4

    return output_grid
```
