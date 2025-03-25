```python
"""
1.  **Identify Non-Black Pixels:** Find all pixels in the input grid that are not black (color 0).
2.  **Identify two distinct objects:** Select two pixels from the identified non-black pixels.
3. **Keep original pixel color:** Create copy of input grid and keep these two pixel with their input color.
4.  **Create a Rectangle:** Imagine a rectangle where these two pixels are opposite corners.
5.  **Fill the Rectangle:** Fill the entire rectangle, including the edges, with yellow (color 4).
"""

import numpy as np

def find_non_black_pixels(grid):
    """Finds the coordinates of non-black pixels."""
    return np.argwhere(grid != 0)

def fill_rectangle(grid, pixel1, pixel2, color):
    """Fills a rectangle defined by two pixels with a given color."""
    min_row = min(pixel1[0], pixel2[0])
    max_row = max(pixel1[0], pixel2[0])
    min_col = min(pixel1[1], pixel2[1])
    max_col = max(pixel1[1], pixel2[1])

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            grid[row, col] = color

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find non-black pixels
    non_black_pixels = find_non_black_pixels(input_grid)

    # Check if there are at least two non-black pixels
    if len(non_black_pixels) >= 2:
        # Select the first two non-black pixels
        pixel1 = non_black_pixels[0]
        pixel2 = non_black_pixels[1]
        
        #Keep the color of the original pixels
        output_grid[pixel1[0], pixel1[1]] = input_grid[pixel1[0], pixel1[1]]
        output_grid[pixel2[0], pixel2[1]] = input_grid[pixel2[0], pixel2[1]]


        # Fill the rectangle with yellow
        fill_rectangle(output_grid, pixel1, pixel2, 4)

    return output_grid
```