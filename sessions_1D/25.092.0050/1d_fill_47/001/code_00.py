"""
Fill the segment between two identical non-white pixels with their color.

Given a 1D input grid (represented as a list or a 1xN array):
1. Identify the single non-white color present.
2. Find all indices where this color appears.
3. Determine the minimum and maximum indices among these.
4. Create a copy of the input grid.
5. Fill the segment in the copied grid from the minimum index to the maximum index (inclusive) with the identified non-white color.
6. Return the modified grid.
"""

import numpy as np

def find_non_white_pixels(grid):
    """
    Finds the non-white color and its indices in a 1D grid.

    Args:
        grid (list or np.ndarray): A 1D list or numpy array representing the grid row.

    Returns:
        tuple: (non_white_color, indices) or (None, []) if no non-white pixel found.
    """
    non_white_color = None
    indices = []
    for i, pixel in enumerate(grid):
        if pixel != 0:
            # If we haven't found a non-white color yet, store it.
            # We assume based on examples that there's only one non-white color.
            if non_white_color is None:
                non_white_color = pixel
            # Check if the current pixel matches the found non-white color
            if pixel == non_white_color:
                indices.append(i)

    return non_white_color, indices

def transform(input_grid):
    """
    Transforms the input grid by filling the segment between the two
    non-white pixels with their color.

    Args:
        input_grid (list or np.ndarray): A 1D grid (or a 2D grid with 1 row).

    Returns:
        list or np.ndarray: The transformed grid in the same format as the input.
    """
    # Ensure we are working with a 1D list or array
    # Handle potential numpy array input or list of lists input
    if isinstance(input_grid, np.ndarray):
        # Flatten if it's multidimensional (like 1xN)
        if input_grid.ndim > 1:
            grid_1d = input_grid.flatten().tolist()
        else:
            grid_1d = input_grid.tolist()
        is_numpy = True
        original_shape = input_grid.shape
    elif isinstance(input_grid, list) and all(isinstance(row, list) for row in input_grid):
        # Handle list of lists (assuming 1 row)
        if len(input_grid) == 1:
            grid_1d = input_grid[0]
            is_list_of_lists = True
        else:
            # This specific transformation seems designed for 1D, raise error or handle differently?
            # For now, assume it's effectively 1D if passed as list of lists with one row.
            # If more rows, the logic might not apply directly. Let's proceed assuming 1 row.
            # Or raise an error if len > 1? Sticking with the assumption for now.
            if len(input_grid) > 1 :
                 raise ValueError("Input grid has more than one row, this function expects a 1D structure.")
            grid_1d = input_grid[0] # Take the first row
            is_list_of_lists = True


    else:
        # Assume it's already a 1D list
        grid_1d = input_grid
        is_numpy = False
        is_list_of_lists = False


    # 1. Identify the non-white color and find its indices
    non_white_color, indices = find_non_white_pixels(grid_1d)

    # If no non-white pixels or only one, return a copy of the input
    # Based on task description, there should be exactly two.
    if non_white_color is None or len(indices) < 2:
        # Return in the original format
        if is_numpy:
            return np.array(grid_1d).reshape(original_shape)
        elif is_list_of_lists:
            return [grid_1d[:]] # Return a copy wrapped in a list
        else:
            return grid_1d[:] # Return a copy

    # 2. Determine the minimum and maximum indices
    min_idx = min(indices)
    max_idx = max(indices)

    # 3. Create a copy of the input grid (as a 1D list for modification)
    output_grid_1d = list(grid_1d) # Use list() for copy

    # 4. Fill the segment from min_idx to max_idx (inclusive)
    for i in range(min_idx, max_idx + 1):
        output_grid_1d[i] = non_white_color

    # 5. Return the modified grid in the original format
    if is_numpy:
        return np.array(output_grid_1d).reshape(original_shape)
    elif is_list_of_lists:
        return [output_grid_1d]
    else:
        return output_grid_1d