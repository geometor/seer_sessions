import numpy as np
import copy

"""
Fill the gap between two identical non-white pixels in a 1D grid.

1. Scan the input grid (1D array) to find the positions (indices) of the two non-white pixels.
2. Identify the color (fill_color) of these two non-white pixels. They will have the same color.
3. Determine the starting index (start_index) and ending index (end_index) of these pixels, where start_index < end_index.
4. Create a copy of the input grid to serve as the initial output grid.
5. Iterate through all indices i from start_index + 1 up to (but not including) end_index.
6. For each index i in this range, change the color of the pixel at that index in the output grid to fill_color.
7. The resulting grid is the final output.
"""

def find_non_white_pixels(grid_row):
    """Finds the indices and color of non-white pixels in a 1D array."""
    indices = []
    color = None
    for idx, pixel_value in enumerate(grid_row):
        if pixel_value != 0:
            indices.append(idx)
            # Store the color of the first non-white pixel found
            if color is None:
                color = pixel_value
            # Optional: Check if subsequent non-white pixels have the same color
            # elif pixel_value != color:
            #     raise ValueError("Non-white pixels have different colors")
    return indices, color

def transform(input_grid):
    """
    Fills the gap between two identical non-white pixels in a 1D grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert to numpy array for easier handling, although list operations work too
    input_np = np.array(input_grid, dtype=int)

    # Since the grid is 1xN, we work with the first (and only) row
    grid_row = input_np[0]

    # Find the indices and the color of the non-white pixels
    non_white_indices, fill_color = find_non_white_pixels(grid_row)

    # Check if exactly two non-white pixels were found (as per observations)
    if len(non_white_indices) != 2 or fill_color is None:
        # If the pattern doesn't match, return the input unchanged or handle error
        # For this specific task based on examples, we expect exactly two markers.
        # If not found, maybe return input as is or raise error? Let's return copy.
        print(f"Warning: Expected 2 non-white pixels, found {len(non_white_indices)}. Returning input copy.")
        return copy.deepcopy(input_grid) # Return a copy to avoid modifying original

    # Determine the start and end indices for filling
    start_index = min(non_white_indices)
    end_index = max(non_white_indices)

    # Create a copy of the input grid to modify
    # Using deepcopy if input is list of lists, or np.copy if numpy array
    output_np = np.copy(input_np)
    output_row = output_np[0] # Get reference to the row in the output array

    # Fill the gap between the start and end indices
    # Iterate from the pixel *after* the first marker up to (not including) the second marker
    for i in range(start_index + 1, end_index):
        output_row[i] = fill_color

    # Convert back to list of lists if necessary, depending on required output format
    output_grid = output_np.tolist()

    return output_grid
