import numpy as np

"""
Identifies two distinct non-zero colored objects in the input grid. Determines which object is vertically higher (Top Object) and which is lower (Bottom Object) based on their minimum row indices. The Bottom Object remains in its original position in the output grid. The Top Object is moved vertically downwards so that its new top edge is positioned one row below the original bottom edge of the Bottom Object. The internal structure and horizontal positions of both objects are preserved. The output grid is initialized with the background color (0).
"""

def find_object_coords_and_bounds(grid, color):
    """
    Finds all coordinates and the row bounds for a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the object to find.

    Returns:
        tuple: A tuple containing:
            - list: A list of (row, col) coordinates for the object.
            - int: The minimum row index of the object.
            - int: The maximum row index of the object.
            Returns ([], -1, -1) if the color is not found.
    """
    coords = []
    min_row = -1
    max_row = -1
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                coords.append((r, c))
                if min_row == -1 or r < min_row:
                    min_row = r
                if r > max_row:
                    max_row = r
    return coords, min_row, max_row

def transform(input_grid):
    """
    Transforms the input grid by identifying two objects and swapping their vertical order.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid)
    rows, cols = grid_np.shape

    # Initialize output_grid with the background color (0)
    output_grid = np.zeros_like(grid_np)

    # Find the unique non-zero colors in the input grid
    unique_colors = np.unique(grid_np[grid_np != 0])

    if len(unique_colors) != 2:
        # Handle cases with not exactly two colors if necessary,
        # for now, assume valid input based on examples
        return input_grid # Or raise an error, or return empty grid

    color_a = unique_colors[0]
    color_b = unique_colors[1]

    # Find coordinates and row bounds for each object
    coords_a, min_row_a, max_row_a = find_object_coords_and_bounds(grid_np, color_a)
    coords_b, min_row_b, max_row_b = find_object_coords_and_bounds(grid_np, color_b)

    # Identify the Top and Bottom objects based on minimum row index
    if min_row_a < min_row_b:
        top_color, top_coords, min_row_top = color_a, coords_a, min_row_a
        bottom_color, bottom_coords, max_row_bottom = color_b, coords_b, max_row_b
    else:
        top_color, top_coords, min_row_top = color_b, coords_b, min_row_b
        bottom_color, bottom_coords, max_row_bottom = color_a, coords_a, max_row_a

    # Calculate the vertical shift needed for the Top Object
    # The new top row of the Top Object should be one row below the max row of the Bottom Object
    shift = (max_row_bottom + 1) - min_row_top

    # Populate the output grid
    # Place the Bottom Object at its original location
    for r, c in bottom_coords:
        output_grid[r, c] = bottom_color

    # Place the Top Object at its new shifted location
    for r, c in top_coords:
        new_r = r + shift
        # Check bounds just in case, though problem description implies shapes fit
        if 0 <= new_r < rows:
             output_grid[new_r, c] = top_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()