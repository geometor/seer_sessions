import numpy as np

"""
Identify rows and columns composed entirely of red (2) pixels in the input grid.
Construct an output grid containing only these complete red rows and columns,
superimposed on a white (0) background. All other pixels are set to white (0).
"""

# Constants for color values
RED = 2
WHITE = 0

def _find_full_red_rows(grid):
    """
    Identifies the indices of rows in the grid that consist entirely of RED pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of row indices that are completely red.
    """
    rows, _ = grid.shape
    full_rows = []
    for r in range(rows):
        # Check if all elements in the current row are RED
        if np.all(grid[r, :] == RED):
            full_rows.append(r)
    return full_rows

def _find_full_red_cols(grid):
    """
    Identifies the indices of columns in the grid that consist entirely of RED pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of column indices that are completely red.
    """
    _, cols = grid.shape
    full_cols = []
    for c in range(cols):
        # Check if all elements in the current column are RED
        if np.all(grid[:, c] == RED):
            full_cols.append(c)
    return full_cols

def transform(input_grid_list):
    """
    Transforms the input grid by keeping only the complete horizontal and vertical
    lines of red pixels found in the input.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # Initialize a boolean mask grid of the same dimensions, initially all False.
    # This mask will mark pixels that should be red in the output.
    mask = np.full((rows, cols), False, dtype=bool)

    # Identify rows consisting entirely of RED
    full_red_rows = _find_full_red_rows(input_grid)
    # For each full red row found, set the corresponding row in the mask to True
    for r_idx in full_red_rows:
        mask[r_idx, :] = True

    # Identify columns consisting entirely of RED
    full_red_cols = _find_full_red_cols(input_grid)
    # For each full red column found, set the corresponding column in the mask to True
    for c_idx in full_red_cols:
        mask[:, c_idx] = True

    # Create the output grid, initialized with the background color (WHITE)
    output_grid = np.full((rows, cols), WHITE, dtype=int)

    # Apply the mask: Where the mask is True, set the output grid pixel to RED
    output_grid[mask] = RED

    # Convert the numpy array back to a list of lists for the required output format
    return output_grid.tolist()
