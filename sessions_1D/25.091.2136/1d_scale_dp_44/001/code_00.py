"""
Identify contiguous blocks of white pixels (color 0) in the input 1D grid.
If a white block is immediately preceded by a non-white pixel AND immediately followed by a non-white pixel, replace all pixels in that white block with the color of the preceding non-white pixel.
Otherwise, leave the white block unchanged.
Non-white pixels are never changed.
"""

import numpy as np

def transform(input_grid_list):
    """
    Transforms the input 1D grid based on the rules described above.

    Args:
        input_grid_list (list): A list of integers representing the input grid (1D).

    Returns:
        list: The transformed list representing the output grid.
    """
    # Ensure input is a list for easier manipulation, even if it comes as a numpy array row
    if isinstance(input_grid_list, np.ndarray):
      # Assuming it's a 1D array or a row from a 2D array
      input_grid = input_grid_list.flatten().tolist()
    else:
      # Make a copy to avoid modifying the original input if it's mutable
      input_grid = list(input_grid_list) 

    output_grid = list(input_grid) # Create a mutable copy for the output
    n = len(input_grid)
    i = 0
    
    # Iterate through the grid
    while i < n:
        # Check if the current pixel is white
        if input_grid[i] == 0:
            # Find the end of the contiguous block of white pixels
            j = i
            while j + 1 < n and input_grid[j + 1] == 0:
                j += 1
            
            # Check if the block is 'sandwiched' by non-white pixels
            is_preceded_by_non_white = (i > 0 and input_grid[i - 1] != 0)
            is_followed_by_non_white = (j < n - 1 and input_grid[j + 1] != 0)
            
            # If the block is sandwiched, fill it with the preceding color
            if is_preceded_by_non_white and is_followed_by_non_white:
                fill_color = input_grid[i - 1]
                for k in range(i, j + 1):
                    output_grid[k] = fill_color
            
            # Move the pointer past the processed block
            i = j + 1
        else:
            # If the current pixel is not white, move to the next pixel
            i += 1
            
    return output_grid