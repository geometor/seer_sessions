# e8dc4411 • 010 • example_2 • investigate_coder

---
```python
"""
Locate a cross shape made of white pixels, find the green pixel at its center,
and expand the green pixel downwards and to the sides in an inverted triangle
shape, replacing blue pixels.
"""

import numpy as np

def find_cross_center(grid):
    # Find white pixels
    white_pixels = np.argwhere(grid == 0)
    if len(white_pixels) == 0:
        return None

    # Calculate centroid of white pixels
    centroid = white_pixels.mean(axis=0)

    # Find the white pixel closest to the centroid
    distances = np.sqrt(np.sum((white_pixels - centroid)**2, axis=1))
    center_index = np.argmin(distances)
    center_pixel = white_pixels[center_index]
    
    #check that it is a cross - 5 white pixels
    
    x,y = center_pixel
    cross_pixels = [(x,y), (x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    cross_count = 0
    for pixel in cross_pixels:
        if 0 <= pixel[0] < grid.shape[0] and 0 <= pixel[1] < grid.shape[1] and grid[pixel[0], pixel[1]] == 0:
            cross_count +=1

    if cross_count != 5:
        return None

    return tuple(center_pixel)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the center of the white cross
    cross_center = find_cross_center(input_grid)
    if cross_center is None:
        return output_grid

    # Get the coordinates of the green pixel (center of the cross)
    green_row, green_col = cross_center

    if input_grid[green_row, green_col] != 3:
        # check pixel above
        if input_grid[green_row -1, green_col] == 3:
            green_row = green_row - 1
        else:
            return output_grid

    # Expand the green pixel downwards
    for row in range(green_row + 1, output_grid.shape[0]):
        # Calculate the extent of the expansion
        expansion = row - green_row
        
        # Apply the expansion to the left and right
        for col in range(green_col - expansion, green_col + expansion + 1):
            if 0 <= col < output_grid.shape[1]:
                output_grid[row, col] = 3

    return output_grid
```
