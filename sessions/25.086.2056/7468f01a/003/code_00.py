"""
The transformation identifies the smallest rectangular region (bounding box) that encompasses all non-white (color 0) pixels in the input grid. This subgrid is then extracted. Finally, the extracted subgrid is flipped horizontally (reflected across its vertical axis) to produce the output grid.
"""

import numpy as np

def find_bounding_box(grid):
    """
    Finds the coordinates of all non-background pixels and calculates their bounding box.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) if non-background pixels exist,
               None otherwise.
    """
    # Find indices of all pixels that are not white (0)
    non_background_pixels = np.argwhere(grid != 0)
    if non_background_pixels.size == 0:
        # Handle the case where the grid is all white or empty
        return None

    # Determine the min/max row and column indices from the non-white pixels
    min_row = non_background_pixels[:, 0].min()
    max_row = non_background_pixels[:, 0].max()
    min_col = non_background_pixels[:, 1].min()
    max_col = non_background_pixels[:, 1].max()

    return min_row, max_row, min_col, max_col

def extract_subgrid(grid, min_row, max_row, min_col, max_col):
    """
    Extracts a subgrid defined by the bounding box coordinates.

    Args:
        grid (np.ndarray): The input grid.
        min_row (int): The minimum row index (inclusive).
        max_row (int): The maximum row index (inclusive).
        min_col (int): The minimum column index (inclusive).
        max_col (int): The maximum column index (inclusive).

    Returns:
        np.ndarray: The extracted subgrid.
    """
    # Extract the subgrid using numpy slicing
    # Add 1 to max_row and max_col because slicing is exclusive of the upper bound
    return grid[min_row:max_row + 1, min_col:max_col + 1]

def transform(input_grid):
    """
    Extracts the bounding box of non-white pixels and flips it horizontally.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)

    # Step 1: Find the bounding box of the non-white object(s)
    bounding_box = find_bounding_box(input_grid_np)

    # Handle the edge case where no non-white pixels are found
    if bounding_box is None:
        # Return an empty grid or the original grid, depending on task requirements.
        # Based on examples, we expect content, so return an empty list or handle appropriately.
        # Returning an empty grid seems reasonable if the input was all white.
        return [[]]

    min_row, max_row, min_col, max_col = bounding_box

    # Step 2: Extract the subgrid defined by the bounding box
    extracted_subgrid = extract_subgrid(input_grid_np, min_row, max_row, min_col, max_col)

    # Step 3: Flip the extracted subgrid horizontally
    # np.fliplr flips an array in the left/right direction
    flipped_subgrid = np.fliplr(extracted_subgrid)

    # Step 4: Convert the resulting NumPy array back to a list of lists
    output_grid = flipped_subgrid.tolist()

    return output_grid