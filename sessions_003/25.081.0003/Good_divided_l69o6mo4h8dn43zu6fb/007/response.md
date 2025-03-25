```python
"""
The transformation rule involves removing pixels of color 4 (yellow) and 2 (red) from the input grid, then shifting the remaining pixels to the top-left, maintaining their original order, and finally filling the remaining spaces with color 0 (white).
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    
    # Create a list to store the non-removed pixels
    remaining_pixels = []
    
    # Iterate through each cell of the grid, collecting non-removed pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 4 and input_grid[r, c] != 2:
                remaining_pixels.append(input_grid[r, c])

    # Fill the output_grid with the remaining pixels, from top-left
    k = 0
    for r in range(rows):
        for c in range(cols):
            if k < len(remaining_pixels):
                output_grid[r, c] = remaining_pixels[k]
                k += 1
            else:
                break
        if k >= len(remaining_pixels): #added condition to stop the process after pixels finish.
            break


    return output_grid
```