"""
Transforms the input grid based on the number of edges touched by non-white pixels.
1. Receive the input grid.
2. Identify all non-white pixels (pixels with value > 0).
3. If there are no non-white pixels, return the input grid unchanged.
4. Determine which of the four grid edges (Top, Bottom, Left, Right) contain at least one non-white pixel. Count how many distinct edges are touched (`E`).
5. Create an intermediate grid by rotating the original input grid 180 degrees.
6. Check the value of `E` calculated in step 4:
    a.  If `E` is exactly 1: Create the final output grid by taking the intermediate (rotated) grid and shifting its content up by 2 rows. Fill the newly empty bottom 2 rows with white pixels (0).
    b.  If `E` is 0, 2, 3, or 4: The final output grid is the intermediate (rotated) grid itself.
7. Return the final output grid.
"""

import numpy as np

def count_edges_touched(grid):
    """
    Counts the number of grid edges (Top, Bottom, Left, Right)
    touched by any non-white pixels (value != 0).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        int: The number of edges touched (0-4).
    """
    height, width = grid.shape

    # Find coordinates of non-white pixels
    non_white_coords = np.argwhere(grid != 0)

    # Handle case where the grid is all white (no non-white pixels)
    if non_white_coords.shape[0] == 0:
        return 0

    # Find the minimum and maximum row and column indices of non-white pixels
    r_min = non_white_coords[:, 0].min()
    r_max = non_white_coords[:, 0].max()
    c_min = non_white_coords[:, 1].min()
    c_max = non_white_coords[:, 1].max()

    # Check if the bounding box of non-white pixels touches each edge
    touches_top = (r_min == 0)
    touches_bottom = (r_max == height - 1)
    touches_left = (c_min == 0)
    touches_right = (c_max == width - 1)

    # Sum the boolean values (True=1, False=0) to get the count
    num_edges_touched = sum([touches_top, touches_bottom, touches_left, touches_right])

    return num_edges_touched

def rotate_180(grid):
    """
    Rotates a 2D numpy array by 180 degrees.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The grid rotated by 180 degrees.
    """
    # Use numpy's rot90 function for efficient 180-degree rotation (k=2)
    return np.rot90(grid, 2)

def shift_up(grid, rows):
    """
    Shifts a grid's content up by a specified number of rows,
    filling the vacated bottom rows with white (0).

    Args:
        grid (np.ndarray): The input grid.
        rows (int): The number of rows to shift up.

    Returns:
        np.ndarray: The shifted grid.
    """
    height, width = grid.shape

    # Initialize the output grid with the background color (white = 0)
    shifted_grid = np.zeros_like(grid)

    # If shifting by 0 or negative rows, no change is needed
    if rows <= 0:
        return grid

    # If shifting by height or more, the result is an all-white grid
    if rows >= height:
        return shifted_grid

    # Copy the portion of the original grid that remains after the shift
    # Source rows: from index 'rows' to the end ('height')
    # Destination rows: from index 0 to 'height - rows'
    shifted_grid[0 : height - rows, :] = grid[rows : height, :]

    return shifted_grid

def transform(input_grid):
    """
    Applies the conditional rotation and shift transformation to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input list of lists to a numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)

    # Step 3: Handle the edge case of an all-white grid. If so, return it unchanged.
    # This is implicitly handled by count_edges_touched returning 0, leading to step 6b.
    # Rotating an all-white grid results in an all-white grid.
    if np.all(grid == 0):
        return input_grid # Return original list of lists format

    # Step 4: Calculate the number of edges touched by non-white pixels in the original grid.
    num_edges = count_edges_touched(grid)

    # Step 5: Rotate the input grid by 180 degrees.
    rotated_grid = rotate_180(grid)

    # Step 6: Check the condition based on the number of edges touched.
    if num_edges == 1:
        # Step 6a: If exactly one edge was touched, shift the rotated grid up by 2 rows.
        output_grid = shift_up(rotated_grid, 2)
    else:
        # Step 6b: Otherwise (0, 2, 3, or 4 edges touched), use the rotated grid directly.
        output_grid = rotated_grid

    # Step 7: Convert the final numpy array back to a list of lists format and return.
    return output_grid.tolist()