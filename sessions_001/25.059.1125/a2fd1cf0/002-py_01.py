"""
1.  **Identify:** Locate the red pixel (value '2') and the green pixel (value '3') within the input grid. These are the start and end points, respectively.
2.  **Path Creation, Method 2 (L-Shape):** Create an "L" shaped path made of azure pixels (8). The path should have a single 90 degree turn.
    - find the row of the red pixel and fill it with azure pixels up until the column which contains the green pixel.
    - then fill the column of the green pixel with azure until reaching the green pixel.
3.  **Output:** Produce the modified grid, where the path connects the start and end pixels.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first pixel of a specified color."""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                return (i, j)
    return None  # Should not happen in this specific task, but good practice

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find start (red) and end (green) pixels
    start_pixel = find_pixel(input_grid, 2)
    end_pixel = find_pixel(input_grid, 3)
    
    # Create the L-shaped path
    if start_pixel and end_pixel:
        # Fill the row of the red pixel with azure until the green pixel's column
        for j in range(min(start_pixel[1], end_pixel[1]), max(start_pixel[1], end_pixel[1]) +1):
            if output_grid[start_pixel[0],j] != 2:
                output_grid[start_pixel[0], j] = 8
            

        # Fill the column of the green pixel with azure until the green pixel
        for i in range(min(start_pixel[0], end_pixel[0]), max(start_pixel[0],end_pixel[0])+1):
            output_grid[i, end_pixel[1]] = 8

    return output_grid