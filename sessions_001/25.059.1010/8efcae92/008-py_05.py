"""
1.  Examine Input: Receive the input grid.
2.  Identify Non-White Pixels: Locate all pixels that are not white (value 0).
3.  Check for Cross: Determine if the non-white pixels form a "cross" shape. A cross shape is defined as a 3x3 grid where the center row and center column are all the same non-white color, all other values are white, and the center value of the 3x3 grid is also this color.
4.  Conditional Extraction:
    *   If a cross shape is present, return a 1x1 grid containing *only* the center pixel of the cross.
    *   If no cross shape is present, and there is only one non-white pixel, return the single non-white pixel as a 1x1 grid.
    *   If no non-white pixels are present, return an empty grid.
    * If a cross is not present, but other non-cross shapes are present, return just the center of the cross if it was a cross
"""

import numpy as np

def is_cross(grid):
    """Helper function to check for the 'cross' shape."""
    non_white_indices = np.argwhere(grid != 0)
    if len(non_white_indices) < 5:  # A cross needs at least 5 pixels
        return None

    rows, cols = zip(*non_white_indices)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Check for filled center row and center column, with single pixel ends.
    if (max_row - min_row) == 2 and (max_col - min_col) == 2:
        center_row = min_row + 1
        center_col = min_col + 1
        center_value = grid[center_row, center_col]

        # Check that center row and col are all same non-white color
        if (grid[center_row, min_col] == center_value and
            grid[center_row, max_col] == center_value and
            grid[min_row, center_col] == center_value and
            grid[max_row, center_col] == center_value):
            return (center_row, center_col)

    return None

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Find the indices of all non-white (non-zero) pixels.
    non_white_indices = np.argwhere(input_array != 0)

    # If there are no non-white pixels, return an empty grid.
    if non_white_indices.size == 0:
        return np.array([])

    # Check for cross shape.
    cross_center = is_cross(input_array)
    if cross_center:
        row, col = cross_center
        output_grid = np.array([[input_array[row, col]]])
        return output_grid

    # if only one non-white pixel return it
    if non_white_indices.size == 1:
       row, col = non_white_indices[0]
       return np.array([[input_array[row,col]]])


    # Find the minimum and maximum row and column indices to simulate cross
    min_row, min_col = np.min(non_white_indices, axis=0)

    # Extract the subgrid defined by these boundaries to check for cross
    output_grid = input_array[min_row:min_row+3, min_col:min_col+3]

    cross_center = is_cross(output_grid)
    if cross_center:
        row, col = cross_center
        output_grid = np.array([[output_grid[row, col]]])
        return output_grid
    else:
      return np.array([])