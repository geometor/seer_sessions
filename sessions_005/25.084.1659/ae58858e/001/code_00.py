import numpy as np

def find_2x2_red_squares(grid):
    """
    Identifies all pixels that are part of any 2x2 square composed entirely of red (2) pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        np.array: A boolean mask of the same shape as grid, where True indicates
                  a pixel is part of at least one 2x2 red square.
    """
    height, width = grid.shape
    # Initialize a mask to keep track of pixels that need to change color
    change_mask = np.zeros_like(grid, dtype=bool)

    # Iterate through all possible top-left corners of a 2x2 square
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if the 2x2 block starting at (r, c) is all red (2)
            if (grid[r, c] == 2 and
                grid[r+1, c] == 2 and
                grid[r, c+1] == 2 and
                grid[r+1, c+1] == 2):
                # If it is, mark all four pixels in the mask
                change_mask[r, c] = True
                change_mask[r+1, c] = True
                change_mask[r, c+1] = True
                change_mask[r+1, c+1] = True
    return change_mask

def transform(input_grid):
    """
    Transforms the input grid by changing the color of red (2) pixels to magenta (6)
    if they are part of any 2x2 square composed entirely of red pixels.
    Other pixels remain unchanged.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # Create a copy of the input array to modify, this will be the output grid
    output_array = np.copy(input_array)

    # Find all pixels that belong to a 2x2 red square
    pixels_to_change = find_2x2_red_squares(input_array)

    # Change the color of the identified pixels to magenta (6) in the output grid
    output_array[pixels_to_change] = 6

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
