"""
Transforms an input grid by replacing a single non-zero "seed" pixel with a 0 and drawing a rectangular frame of the seed's color around the grid's edges. Pixels adjacent to the original seed pixel are also set to 0, while the rest of the inner pixels are filled with the seed's color.
"""

import numpy as np

def get_seed_pixel(grid):
    # Find the coordinates and value of the non-zero seed pixel.
    non_zero_indices = np.nonzero(grid)
    if len(non_zero_indices[0]) > 0:  # Check if there are any non-zero elements
       x = non_zero_indices[0][0]
       y = non_zero_indices[1][0]
       color = grid[x, y]
       return x, y, color
    return None,None,None # return None values when there is no non-zero values


def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get the seed pixel information
    seed_x, seed_y, seed_color = get_seed_pixel(input_grid)
    
    if seed_x is None:
        return input_grid.tolist()

    # Create the frame with the seed color
    output_grid[0, :] = seed_color          # Top row
    output_grid[-1, :] = seed_color         # Bottom row
    output_grid[:, 0] = seed_color          # Left column
    output_grid[:, -1] = seed_color         # Right column

    # set seed pixel to 0
    output_grid[seed_x, seed_y] = 0

    # Set pixels adjacent to the seed pixel to 0
    if seed_x > 0:
        output_grid[seed_x - 1, seed_y] = 0  # Above
    if seed_x < rows - 1:
        output_grid[seed_x + 1, seed_y] = 0  # Below
    if seed_y > 0:
        output_grid[seed_x, seed_y - 1] = 0  # Left
    if seed_y < cols - 1:
        output_grid[seed_x, seed_y + 1] = 0  # Right
    
    # Fill the rest of the inner grid
    for i in range(rows):
      for j in range(cols):
        if output_grid[i,j] == 0 and not (i==seed_x and j == seed_y): # if the location is currently 0 and isn't the seed pixel
            # check if its within the frame
            if not (i == 0 or i == rows-1 or j == 0 or j == cols-1):
                output_grid[i,j] = seed_color


    return output_grid.tolist()