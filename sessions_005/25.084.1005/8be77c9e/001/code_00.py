"""
Constructs the output grid by stacking the original input grid on top of a vertically flipped (upside-down) version of itself. The resulting output grid has the same width as the input and double the height.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by stacking it above its vertical reflection.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Get the height (H) and width (W) of the input grid
    H, W = input_array.shape
    
    # Create a vertically flipped version of the input grid
    # Slicing [::-1] reverses the order of rows
    reflected_array = input_array[::-1, :]
    
    # Create the output grid by vertically stacking the original and reflected arrays
    # np.vstack combines arrays vertically
    output_array = np.vstack((input_array, reflected_array))
    
    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
