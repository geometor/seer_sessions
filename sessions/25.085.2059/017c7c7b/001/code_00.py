import numpy as np

"""
Transforms the input grid by first changing all blue (1) pixels to red (2), 
keeping white (0) pixels unchanged. Then, it takes the top half 
(H/2 rows, where H is the input height) of this color-modified grid and 
appends it vertically to the bottom of the full color-modified grid. 
The final output grid has a height of 1.5 times the input height and the same width.
"""

def transform(input_grid):
    """
    Applies the color change and vertical concatenation transformation.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Create an intermediate grid by copying the input
    intermediate_grid = input_np.copy()

    # Change all blue (1) pixels to red (2) in the intermediate grid
    intermediate_grid[intermediate_grid == 1] = 2

    # Get the height (H) of the intermediate grid
    H = intermediate_grid.shape[0]

    # Calculate the height of the top half (integer division)
    top_half_height = H // 2

    # Extract the top half of the intermediate grid
    top_half_grid = intermediate_grid[:top_half_height, :]

    # Construct the final output grid by vertically stacking the intermediate grid
    # and its top half
    output_np = np.vstack((intermediate_grid, top_half_grid))

    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
