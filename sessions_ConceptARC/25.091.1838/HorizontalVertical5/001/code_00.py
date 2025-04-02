"""
Transformation Rule:
1. Identify the bounding box of all yellow (4) pixels in the input grid.
2. Determine the height and width of the input grid and the bounding box.
3. Check if the yellow bounding box touches any of the four edges of the input grid.
4. Based on whether the bounding box touches an edge and its aspect ratio (height vs. width), modify the output grid:
    a. If the bounding box touches any edge, set the entire top row (row 0) to green (3).
    b. If the bounding box does not touch any edge AND its height equals its width, set the entire top row (row 0) to green (3).
    c. If the bounding box does not touch any edge AND its width is greater than its height, set the entire rightmost column (column W-1) to green (3).
5. All other pixels retain their original colors from the input grid.
"""

import numpy as np

def find_bounding_box(grid, color):
    """
    Finds the bounding box of all pixels of a given color.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to find.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) if the color exists,
               None otherwise.
    """
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    H, W = input_np.shape

    # Define the target color (yellow) and the modification color (green)
    target_color = 4
    modification_color = 3

    # Find the bounding box of the yellow pixels
    bbox = find_bounding_box(input_np, target_color)

    # If no yellow pixels are found, return the original grid
    if bbox is None:
        return input_grid # Return original list of lists format

    min_r, max_r, min_c, max_c = bbox

    # Calculate bounding box dimensions
    H_obj = max_r - min_r + 1
    W_obj = max_c - min_c + 1

    # Check if the bounding box touches any edge
    touches_edge = (min_r == 0) or (max_r == H - 1) or (min_c == 0) or (max_c == W - 1)

    # Apply the transformation logic
    if touches_edge:
        # If touches edge, fill the top row with green
        output_grid[0, :] = modification_color
    else:
        # If not touching edge, check aspect ratio
        if H_obj == W_obj:
            # If square, fill the top row with green
            output_grid[0, :] = modification_color
        elif W_obj > H_obj:
            # If wider than tall, fill the rightmost column with green
            output_grid[:, W - 1] = modification_color
        # Note: The case H_obj > W_obj is not covered by training examples,
        # so no specific action is taken here based on the observed patterns.

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()