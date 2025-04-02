import numpy as np

"""
Identify the target color from the input grid. The target color is the color 
of the non-white pixel located at the bottom-most, right-most position.
Then, create the output grid by changing the color of all non-white, non-target 
pixels in the input grid to the target color. White pixels and pixels already 
matching the target color remain unchanged.
"""

def find_target_color(grid):
    """
    Finds the target color, which is the color of the non-white pixel
    at the bottom-most, right-most position.
    """
    max_r, max_c = -1, -1
    target_color = 0 # Default to white if no non-white pixel found
    non_white_pixels = []

    # Find all non-white pixels
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                non_white_pixels.append((r, c, grid[r, c]))

    if not non_white_pixels:
      return 0 # Return white if grid is all white

    # Find the maximum row index among non-white pixels
    max_r = -1
    for r, c, color in non_white_pixels:
        if r > max_r:
            max_r = r

    # Filter pixels at the maximum row
    bottom_row_pixels = [(r, c, color) for r, c, color in non_white_pixels if r == max_r]

    # Find the maximum column index among the bottom row pixels
    max_c = -1
    for r, c, color in bottom_row_pixels:
        if c > max_c:
            max_c = c
            target_color = color # Update target color

    return target_color


def transform(input_grid):
    """
    Transforms the input grid based on the identified target color.
    All non-white pixels that are not the target color are changed
    to the target color.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Find the target color
    target_color = find_target_color(input_np)

    # Initialize output_grid as a copy of the input_grid
    output_np = np.copy(input_np)
    height, width = output_np.shape

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            current_color = input_np[r, c]
            # Check if the pixel is non-white and not the target color
            if current_color != 0 and current_color != target_color:
                # Change the color in the output grid to the target color
                output_np[r, c] = target_color

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
