import numpy as np

"""
Transformation Rule:
1. Identify the dimensions of the input grid.
2. Flatten the input grid into a one-dimensional array.
3. Locate the single gray pixel (color 5) and store its index.
4. Identify the color of the contiguous block of non-white (0) and non-gray (5) pixels.
5. Find the indices of all pixels belonging to this colored block.
6. Create a new one-dimensional array of the same size as the flattened input, initialized with the background color (white, 0).
7. Place the gray pixel (color 5) into the new array at its original index.
8. For each index belonging to the colored block, calculate the new index by adding 2 to the original index.
9. Place the color of the block into the new array at each calculated new index.
10. Reshape the new one-dimensional array back into the original grid dimensions.
11. Return the resulting grid.
"""

def find_object_indices(flat_grid, color):
    """Finds the indices of all pixels of a given color in a flattened grid."""
    return np.where(flat_grid == color)[0]

def find_non_background_non_marker_color(flat_grid):
    """Finds the color of the object that is not background (0) or marker (5)."""
    unique_colors = np.unique(flat_grid)
    for color in unique_colors:
        if color != 0 and color != 5:
            return color
    return None # Should not happen based on examples

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Shifts a colored block 2 positions to the right in a flattened representation,
    keeping a gray marker pixel stationary.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    original_shape = input_array.shape

    # Flatten the grid into a 1D array
    flat_input = input_array.flatten()
    grid_size = flat_input.size

    # Initialize the output grid (flattened) with background color (0)
    flat_output = np.zeros_like(flat_input)

    # Find the index of the gray marker pixel (5)
    marker_indices = find_object_indices(flat_input, 5)
    if len(marker_indices) > 0:
        marker_index = marker_indices[0] # Assuming only one marker
        # Place the marker in the output
        flat_output[marker_index] = 5
    else:
        # Handle cases where marker might be missing, though examples show it's always present
        pass 

    # Find the color of the moving object
    moving_object_color = find_non_background_non_marker_color(flat_input)

    if moving_object_color is not None:
        # Find the indices of the moving object
        object_indices = find_object_indices(flat_input, moving_object_color)

        # Calculate the new indices by shifting right by 2
        new_object_indices = object_indices + 2

        # Place the moving object at its new positions in the output
        # Ensure indices are within bounds (although not strictly needed based on examples)
        valid_new_indices = new_object_indices[new_object_indices < grid_size]
        flat_output[valid_new_indices] = moving_object_color

    # Reshape the flattened output array back to the original grid dimensions
    output_grid = flat_output.reshape(original_shape)

    # Convert numpy array back to list of lists for standard ARC output
    return output_grid.tolist()
