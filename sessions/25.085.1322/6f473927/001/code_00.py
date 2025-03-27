"""
Create a modified copy of the input grid where red (2) pixels are changed to azure (8). 
Then, create the output grid by horizontally concatenating the modified grid (on the left) 
with the original input grid (on the right). The output grid will have the same height 
as the input grid and double its width.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # 1. Create a copy of the input grid (modified_grid)
    modified_grid = np.copy(input_array)

    # 2. & 3. Iterate through each pixel in the modified_grid and replace red (2) with azure (8)
    # Find indices where the value is 2 (red)
    red_indices = np.where(modified_grid == 2)
    # Change the color at these indices to 8 (azure)
    modified_grid[red_indices] = 8

    # 4. Create the output grid by placing the modified_grid on the left and the original input grid on the right
    # Concatenate along the second axis (axis=1) for horizontal stacking
    output_grid = np.concatenate((modified_grid, input_array), axis=1)

    return output_grid
