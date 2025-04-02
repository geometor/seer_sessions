import numpy as np

"""
Identifies the two non-white pixels in a 1D input grid. 
Changes all white pixels located strictly between these two non-white pixels to the same non-white color. 
Pixels outside this range and the non-white pixels themselves remain unchanged.
"""

def find_non_white_pixels(grid_row):
    """
    Finds the color and indices of the two non-white pixels in a 1D array.

    Args:
        grid_row: A 1D numpy array representing a row of the grid.

    Returns:
        A tuple containing:
        - non_white_color: The integer value (color) of the non-white pixels.
        - indices: A list containing the two indices where the non-white color is found.
        Returns (None, []) if fewer or more than two non-white pixels are found, 
        or if the two non-white pixels have different colors.
    """
    non_white_color = None
    indices = []
    for index, pixel_value in enumerate(grid_row):
        if pixel_value != 0:
            if non_white_color is None:
                non_white_color = pixel_value
            elif pixel_value != non_white_color:
                 # Found a second, different non-white color - invalid input based on rules
                 return None, []
            indices.append(index)

    if len(indices) != 2:
        # Constraint violated: Must have exactly two non-white pixels
        return None, []
        
    return non_white_color, indices

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid. 
                    Expected to be a 1xN grid for this task.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Check if the input is 1D (1 row)
    if input_array.shape[0] != 1:
        # This rule specifically applies to 1D grids as observed
        # Return a copy if the dimensionality is wrong, or handle error as appropriate
        return input_grid 
        
    input_row = input_array[0]

    # Initialize output_grid as a copy of the input
    output_row = np.copy(input_row)

    # 1. & 2. Identify the non-white color and locate the indices
    non_white_color, indices = find_non_white_pixels(input_row)

    # Check if exactly two markers of the same color were found
    if non_white_color is None or not indices:
        # If constraints aren't met, return the original grid unchanged
        return input_grid 

    # Determine the start and end indices for filling
    start_index = min(indices)
    end_index = max(indices)

    # 4. & 5. Iterate between the indices and fill with the non-white color
    # The range goes from start_index + 1 up to (but not including) end_index.
    for i in range(start_index + 1, end_index):
        # Check if the pixel is currently white (optional, but follows description)
        # If output_row[i] == 0: 
        output_row[i] = non_white_color

    # 6. Return the modified grid (converting back to list of lists)
    output_grid = [output_row.tolist()]
    return output_grid