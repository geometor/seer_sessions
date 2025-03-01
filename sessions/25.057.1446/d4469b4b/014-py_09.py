"""
The transformation extracts the 3x3 subgrid centered around the green pixels (value 3) in the input grid and changes the green pixels to gray (value 5) in the output, while keeping white pixels unchanged.
"""

import numpy as np

def get_green_center(grid):
    # Find coordinates of green pixels (value 3)
    green_coords = np.argwhere(grid == 3)
    if green_coords.size == 0:
        return None
    
    # Calculate the average x and y coordinates
    center_y = int(np.floor(np.mean(green_coords[:, 0])))
    center_x = int(np.floor(np.mean(green_coords[:, 1])))
    return (center_y, center_x)

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    
    # Get the center coordinates based on green pixels
    center = get_green_center(input_grid)
    if center is None:
        return input_grid.tolist()

    center_y, center_x = center
    
    # Initialize output_grid with zeros, assuming a 3x3 output
    output_grid = np.zeros((3, 3), dtype=int)

    # Define the boundaries of the 3x3 subgrid in the input grid
    start_y = max(0, center_y - 1)
    end_y = min(input_grid.shape[0], center_y + 2)
    start_x = max(0, center_x - 1)
    end_x = min(input_grid.shape[1], center_x + 2)


    # Extract the 3x3 subgrid from input and map to output grid.
    y_offset = 0
    for y in range(start_y, end_y):
        x_offset = 0
        for x in range(start_x, end_x):

            if y_offset < 3 and x_offset < 3:
                output_grid[y_offset, x_offset] = input_grid[y,x]

            x_offset +=1
        y_offset += 1


    # Change green (3) to gray (5) in the output grid
    output_grid[output_grid == 3] = 5

    return output_grid.tolist()