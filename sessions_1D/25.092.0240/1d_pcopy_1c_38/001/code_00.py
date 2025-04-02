import numpy as np

"""
Identify the single non-white object in the input grid. Determine its color 
and its minimal bounding box (the smallest rectangle containing all its pixels).
Create the output grid by copying the input grid, then filling the entire area 
within the determined bounding box with the identified object's color.
"""

def find_object_and_bounds(grid_np):
    """
    Finds the coordinates and color of the non-white object and its bounding box.

    Args:
        grid_np: A numpy array representing the input grid.

    Returns:
        A tuple containing:
        - object_color: The color (int) of the non-white object. Returns None if no object found.
        - min_row, max_row, min_col, max_col: The bounding box coordinates. Returns None for all if no object found.
    """
    # Find coordinates of all non-white pixels (where value != 0)
    non_white_coords = np.argwhere(grid_np != 0)

    # If no non-white pixels are found, return None
    if non_white_coords.size == 0:
        return None, None, None, None, None

    # Get the color of the first non-white pixel found (assuming only one color)
    object_color = int(grid_np[non_white_coords[0, 0], non_white_coords[0, 1]])

    # Determine the min/max row and column indices
    min_row = non_white_coords[:, 0].min()
    max_row = non_white_coords[:, 0].max()
    min_col = non_white_coords[:, 1].min()
    max_col = non_white_coords[:, 1].max()

    return object_color, min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by finding the non-white object, determining its 
    bounding box, and filling that box with the object's color in the output grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Find the object color and its bounding box coordinates
    object_color, min_row, max_row, min_col, max_col = find_object_and_bounds(input_np)

    # If no object was found, return the original grid
    if object_color is None:
        return input_np

    # Create a copy of the input grid to modify as the output grid
    output_grid = np.copy(input_np)

    # Fill the bounding box area in the output grid with the object's color
    # Note: max_row and max_col are inclusive, so we need +1 for numpy slicing
    output_grid[min_row : max_row + 1, min_col : max_col + 1] = object_color

    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if required by testing framework