import numpy as np

"""
Transformation Rule:
Iterate through the input grid (which is always 1xN).
Identify contiguous horizontal segments of non-white pixels.
If a segment consists of a single non-white pixel (length 1) at index 'i' with color 'c':
  Expand this pixel into a horizontal segment of length 3, centered at index 'i', with the same color 'c'.
  This means changing the pixels at indices 'i-1', 'i', and 'i+1' to color 'c', provided these indices are within the grid boundaries.
Segments with length other than 1 (e.g., 3) and white pixels remain unchanged unless overwritten by an expanding single pixel.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the identified rule.

    Args:
        input_grid (np.ndarray): A 1xN numpy array representing the input grid.

    Returns:
        np.ndarray: A 1xN numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    input_grid_np = np.array(input_grid)

    # Get dimensions (height should be 1)
    height, width = input_grid_np.shape
    if height != 1:
        # This specific rule is designed for 1D grids represented as 1xN
        # Handle potential errors or unexpected shapes if necessary
        # For now, we assume the input conforms to the examples
        pass

    # Initialize output_grid as a copy of the input
    output_grid_np = input_grid_np.copy()
    # Work with the single row for simplicity
    input_row = input_grid_np[0]
    output_row = output_grid_np[0]

    # Iterate through the row to find and process segments
    i = 0
    while i < width:
        current_color = input_row[i]

        # Skip white pixels
        if current_color == 0:
            i += 1
            continue

        # Found a non-white pixel, find the end of the segment
        segment_start = i
        segment_color = current_color
        j = i + 1
        while j < width and input_row[j] == segment_color:
            j += 1
        segment_end = j # segment_end is exclusive index
        segment_length = segment_end - segment_start

        # Apply transformation rule based on segment length
        if segment_length == 1:
            # Expand the single pixel to a length of 3, centered at 'i'
            # Calculate the target indices, clamping to grid boundaries
            target_start = max(0, i - 1)
            target_end = min(width, i + 2) # exclusive index for slicing

            # Modify the output row
            for k in range(target_start, target_end):
                output_row[k] = segment_color

        # For segments of length other than 1 (like 3 in the examples),
        # no action is needed as the output is already a copy.

        # Move the index past the processed segment
        i = segment_end

    # The output_grid_np already holds the modified row
    return output_grid_np
