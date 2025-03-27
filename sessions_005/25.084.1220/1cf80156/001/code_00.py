import numpy as np

"""
Identifies the non-white object in the input grid, determines its bounding box, 
and extracts this bounding box region as the output grid.
"""

def find_bounding_box(grid):
    """
    Finds the coordinates of the bounding box for non-white pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if no non-white pixels found.
    """
    non_white_coords = np.argwhere(grid > 0)
    if non_white_coords.size == 0:
        return None  # No non-white pixels found
    min_row = non_white_coords[:, 0].min()
    max_row = non_white_coords[:, 0].max()
    min_col = non_white_coords[:, 1].min()
    max_col = non_white_coords[:, 1].max()
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Extracts the bounding box of the non-white object from the input grid.

    Args:
        input_grid (list of lists): The input grid representing pixels.

    Returns:
        list of lists: The extracted bounding box region.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)

    # Find the bounding box coordinates of the non-white pixels
    bbox = find_bounding_box(input_array)

    # If no non-white pixels are found, return an empty grid or handle appropriately
    # Based on examples, there's always a non-white object, but handling the edge case is good.
    if bbox is None:
        return [[]] # Or perhaps return the original grid, or raise an error

    min_row, max_row, min_col, max_col = bbox

    # Extract the subgrid defined by the bounding box
    # Slicing includes the start index but excludes the end index, so add 1 to max indices
    output_array = input_array[min_row : max_row + 1, min_col : max_col + 1]

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid