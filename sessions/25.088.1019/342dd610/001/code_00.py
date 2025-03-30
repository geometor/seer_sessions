import numpy as np

"""
Transformation Rule:
1. Create the output grid as a copy of the input grid.
2. Identify the background color (azure, 8).
3. Find all pixels in the input grid that are *not* the background color (foreground pixels). Record their positions (row, column) and their color. Assume all these foreground pixels have the same color.
4. Determine the shift amount (delta_row, delta_col) based on the foreground color:
    - Orange (7): (-2, 0) (Up 2)
    - Red (2): (0, -2) (Left 2)
    - Maroon (9): (+2, 0) (Down 2)
    - Blue (1): (0, +1) (Right 1)
5. Iterate through the original positions of the foreground pixels.
6. For each original position (row, col):
    a. Set the pixel at (row, col) in the output grid to the background color (azure, 8).
    b. Calculate the new position: new_row = row + delta_row, new_col = col + delta_col.
    c. Set the pixel at (new_row, new_col) in the output grid to the foreground color.
7. Return the final output grid.
"""

def find_foreground_pixels(grid, background_color):
    """Finds all pixels not matching the background color."""
    foreground_pixels = []
    foreground_color = -1 # Sentinel value
    coords = np.argwhere(grid != background_color)
    if coords.size > 0:
        foreground_color = grid[coords[0, 0], coords[0, 1]]
        for r, c in coords:
            foreground_pixels.append(((r, c), foreground_color))
    return foreground_pixels, foreground_color

def determine_shift(color):
    """Determines the (delta_row, delta_col) shift based on color."""
    if color == 7:  # orange
        return (-2, 0)
    elif color == 2:  # red
        return (0, -2)
    elif color == 9:  # maroon
        return (+2, 0)
    elif color == 1:  # blue
        return (0, +1)
    else:
        # Default shift if color not recognized (or no foreground found)
        return (0, 0) 

def transform(input_grid):
    """
    Shifts foreground pixels within a grid based on their color.
    The background color (azure, 8) remains static, filling the original
    positions of the moved foreground pixels.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    # Define the background color
    background_color = 8
    
    # Find all foreground pixels and their color
    foreground_pixels, foreground_color = find_foreground_pixels(input_grid_np, background_color)

    # If no foreground pixels are found, return the original grid
    if not foreground_pixels:
        return output_grid.tolist() # Convert back to list of lists

    # Determine the shift based on the foreground color
    delta_row, delta_col = determine_shift(foreground_color)

    # Store the new positions before modifying the grid
    new_positions = []
    for (r, c), color in foreground_pixels:
        new_row = r + delta_row
        new_col = c + delta_col
        new_positions.append(((new_row, new_col), color))

    # Clear the original positions of foreground pixels in the output grid
    for (r, c), _ in foreground_pixels:
         # Check bounds just in case, although not strictly necessary if input follows pattern
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
           output_grid[r, c] = background_color

    # Place the foreground pixels at their new positions in the output grid
    for (new_r, new_c), color in new_positions:
        # Check if the new position is within the grid boundaries
        if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
            output_grid[new_r, new_c] = color
        # else: # Handle cases where pixels move off-grid if necessary (not seen in examples)
        #     pass 

    # Return the modified grid as a list of lists
    return output_grid.tolist()