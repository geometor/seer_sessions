```python
"""
Identifies blue (1) pixels in the input grid and creates green (3) pixels around them, 
forming a specific horizontal pattern centered and in the same row as the blue pixels.
"""

import numpy as np

def find_blue_pixels(grid):
    """Finds the coordinates of all blue (1) pixels in the grid."""
    blue_pixels = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == 1:
                blue_pixels.append((r_idx, c_idx))
    return blue_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    blue_pixels = find_blue_pixels(input_grid)

    # if no blue pixels return the original grid
    if not blue_pixels:
        return output_grid.tolist()

    # sort blue pixels by column
    blue_pixels.sort(key=lambda x: x[1])

    # Create green pixels in the same row.
    if len(blue_pixels) >= 1:
        row = blue_pixels[0][0]  # Row remains the same

        leftmost_blue_col = blue_pixels[0][1]
        
        # Place green pixel to the immediate right.
        if leftmost_blue_col + 1 < input_grid.shape[1]:
            output_grid[row, leftmost_blue_col + 1] = 3
        output_grid[row, leftmost_blue_col] = 3

        
        if len(blue_pixels) > 1:
            rightmost_blue_col = blue_pixels[-1][1]
            
            # Place green pixel to the immediate left of the rightmost blue
            if rightmost_blue_col -1 >= 0:
                output_grid[row, rightmost_blue_col - 1] = 3

            # place a green in the middle
            middle_col = (leftmost_blue_col + rightmost_blue_col) // 2
            output_grid[row, middle_col] = 3
            output_grid[row, rightmost_blue_col] = 3
            

    return output_grid.tolist()
```
