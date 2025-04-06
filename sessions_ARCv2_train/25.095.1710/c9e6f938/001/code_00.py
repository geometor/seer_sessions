import numpy as np

"""
Takes an input grid, creates a horizontally flipped version of it, and 
concatenates the original grid and the flipped grid side-by-side 
(original on the left, flipped on the right) to produce the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by concatenating it with its horizontal mirror image.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the output 2D grid, which is the original
        grid concatenated horizontally with its flipped version.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    grid_np = np.array(input_grid)

    # Create a horizontally flipped version of the input grid
    # Slicing [:, ::-1] reverses the order of columns (axis=1)
    flipped_grid_np = grid_np[:, ::-1]

    # Concatenate the original grid and the flipped grid horizontally
    # axis=1 specifies concatenation along the columns
    output_grid_np = np.concatenate((grid_np, flipped_grid_np), axis=1)

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
