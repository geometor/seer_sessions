import numpy as np

def find_non_background_pixels(input_array):
    """
    Finds the non-background color and the indices of its occurrences.

    Args:
        input_array: A 1D list or numpy array representing the input pixels.

    Returns:
        A tuple containing:
          - non_background_color: The color value (int) that is not 0.
                                   Returns None if only background color is present.
          - indices: A list of indices where the non_background_color appears.
                     Returns an empty list if no non-background color is found.
    """
    non_background_color = None
    indices = []
    for i, pixel in enumerate(input_array):
        if pixel != 0:
            # If this is the first non-background pixel found, store its color
            if non_background_color is None:
                non_background_color = pixel
            # Only track indices matching the first non-background color found
            # (Assuming only one non-background color per input line as per examples)
            if pixel == non_background_color:
                indices.append(i)
    return non_background_color, indices

def transform(input_grid):
    """
    Transforms the input 1D grid by finding two pixels of the same non-background
    color and filling the segment between them (inclusive) with that color.
    Pixels outside this segment remain unchanged (background color 0).
    """
    # The input is expected to be a 1D list or array.
    # If it's nested (like a 1xN array), flatten it.
    if isinstance(input_grid, (list, np.ndarray)) and len(input_grid) == 1 and isinstance(input_grid[0], (list, np.ndarray)):
         input_array = list(input_grid[0])
    elif isinstance(input_grid, np.ndarray):
        input_array = input_grid.tolist() # Convert numpy array to list for easier manipulation
    else:
         input_array = list(input_grid) # Assume it's already a 1D list-like structure

    # Initialize output_array as a copy of the input
    output_array = list(input_array) # Make a copy

    # Find the non-background color and its indices
    non_background_color, indices = find_non_background_pixels(input_array)

    # Proceed only if a non-background color and at least two markers are found
    if non_background_color is not None and len(indices) >= 2:
        # Find the start and end indices of the segment to fill
        start_index = min(indices)
        end_index = max(indices)

        # Fill the segment in the output array
        for i in range(start_index, end_index + 1):
            output_array[i] = non_background_color

    # Return the modified array (potentially nested back if needed, but task seems 1D)
    # For consistency with potential ARC usage, wrap in a list if it was originally.
    # Based on the input format string, it seems like a flat list is expected.
    # Let's return a numpy array as often used in ARC contexts.
    return np.array(output_array, dtype=int) # Return as numpy array
