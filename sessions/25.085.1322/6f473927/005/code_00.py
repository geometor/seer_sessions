import numpy as np

"""
Create the output grid by horizontally concatenating the original input grid 
(on the left) with a modified copy of the input grid (on the right). 
The modified copy is created by changing all red (2) pixels to azure (8). 
The output grid will have the same height as the input grid and double its width.
"""

def transform(input_grid):
    """
    Transforms the input grid by concatenating the original grid horizontally 
    with a modified version where red is replaced by azure.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # 1. Receive the input grid and convert to numpy array.
    input_array = np.array(input_grid, dtype=int)

    # 2. Create a duplicate of the input grid, called modified_grid.
    modified_grid = np.copy(input_array)

    # 3. Iterate through each pixel in the modified_grid. 
    #    If a pixel's color is red (2), change its color to azure (8).
    # Find indices where the value is 2 (red) in the modified grid
    red_indices = np.where(modified_grid == 2)
    # Change the color at these indices to 8 (azure)
    modified_grid[red_indices] = 8

    # 4. Create the output grid by horizontally concatenating the original 
    #    input_array on the left and the modified_grid on the right.
    # Concatenate along the second axis (axis=1) for horizontal stacking
    output_grid = np.concatenate((input_array, modified_grid), axis=1)

    # 5. Return the final output grid
    return output_grid