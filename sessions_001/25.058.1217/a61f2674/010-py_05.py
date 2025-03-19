"""
1.  **Identify:** Find the vertical line of gray (5) pixels in the center column of the input grid.
2.  **Replace:** In the output grid, change the color of this center line from gray (5) to blue (1), keeping the same location and length.
3.  **Identify Left:** Identify all other gray pixels to the left of the center line.
4.  **Consolidate and Transform**: Take x=2, and create a red (2) area starting at the y position of each gray area, and extend it all the way down to the bottom of the grid.
"""

import numpy as np

def find_vertical_line(grid, color):
    """Finds a vertical line of the specified color."""
    height, width = grid.shape
    center_column = width // 2
    line_indices = []
    for row in range(height):
        if grid[row, center_column] == color:
            line_indices.append((row, center_column))
    return line_indices

def find_pixels_left_of_line(grid, line_indices, color):
    """Finds pixels of a specific color to the left of a line"""
    left_pixels = []
    line_x = line_indices[0][1] if line_indices else -1 #get x coordinate
    
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row,col] == color and col < line_x:
                left_pixels.append((row,col))
    return left_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Find the vertical gray line in center
    gray_line_indices = find_vertical_line(input_grid, 5)

    # Replace the gray line with a blue line
    for row, col in gray_line_indices:
        output_grid[row, col] = 1

    # Find other gray pixels to the left
    scattered_gray_pixels = find_pixels_left_of_line(input_grid, gray_line_indices, 5)

    #create red area at x=2
    red_x = 2
    for row, _ in scattered_gray_pixels:
        for y in range(row, height):
            output_grid[y,red_x] = 2
            

    return output_grid