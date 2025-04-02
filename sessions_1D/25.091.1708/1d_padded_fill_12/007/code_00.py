"""
Identifies the single non-white color and all its locations in the input grid.
Determines the overall minimum (global_min_col) and maximum (global_max_col) column indices occupied by any non-white pixel across the entire grid.
Initializes the output grid as a copy of the input grid.
Iterates through each row of the input grid. If a row contains at least one non-white pixel, the corresponding row in the output grid is modified: the segment from global_min_col to global_max_col (inclusive) is filled with the non-white color. Rows without any non-white pixels remain unchanged.
"""

import numpy as np

def find_non_white_pixels(grid_np):
    """
    Finds the non-white color and coordinates of all non-white pixels.

    Args:
        grid_np (np.ndarray): The input grid as a NumPy array.

    Returns:
        tuple: A tuple containing:
            - int: The non-white color value (or 0 if none found).
            - np.ndarray: A 2D NumPy array of shape (N, 2) containing the
                          [row, col] coordinates of N non-white pixels.
                          Returns an empty array if no non-white pixels exist.
    """
    non_white_coords = np.argwhere(grid_np > 0)
    if non_white_coords.size == 0:
        return 0, non_white_coords # No non-white pixels

    # Assuming only one non-white color exists in the grid based on examples
    # Get the color from the first non-white pixel found
    non_white_color = grid_np[non_white_coords[0, 0], non_white_coords[0, 1]]

    return non_white_color, non_white_coords

def transform(input_grid):
    """
    Applies the global horizontal span fill transformation.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize the output array as a copy of the input
    output_array = np.copy(input_array)
    
    # Find the non-white color and all non-white pixel coordinates
    fill_color, non_white_coords = find_non_white_pixels(input_array)

    # If there are no non-white pixels, return the unchanged grid
    if non_white_coords.size == 0:
        return output_array.tolist()

    # Determine the global minimum and maximum column indices from non-white pixels
    global_min_col = np.min(non_white_coords[:, 1])
    global_max_col = np.max(non_white_coords[:, 1])

    # Identify the unique rows that contain non-white pixels
    rows_with_non_white = np.unique(non_white_coords[:, 0])

    # Iterate through the rows identified as containing non-white pixels
    for r in rows_with_non_white:
        # Fill the segment from global_min_col to global_max_col (inclusive)
        # in the corresponding row of the output array with the fill_color.
        output_array[r, global_min_col:global_max_col + 1] = fill_color
        
    # Convert the output NumPy array back to a list of lists
    return output_array.tolist()