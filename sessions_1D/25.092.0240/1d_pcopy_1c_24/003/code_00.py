import numpy as np
import copy

"""
Transforms a 1D input grid (represented as a 1xN list of lists or NumPy array) 
by expanding isolated non-white pixels horizontally.

An 'isolated_pixel' pattern is identified when a non-white pixel (color C > 0) 
at index 'i' has white neighbors (color 0) at both index 'i-1' and index 'i+1'.

For each identified pattern in the original input grid, the corresponding 
white neighbors at indices 'i-1' and 'i+1' in the output grid are changed 
to the color C of the central pixel at index 'i'. The central pixel itself 
remains unchanged (or is effectively overwritten with its own color). 
Pixels not involved in such a pattern are copied unchanged from input to output.

The transformation is based solely on patterns found in the original input grid; 
changes made during the process do not influence the detection of other patterns 
within the same transformation step.
"""

def transform(input_grid):
    """
    Applies the isolated pixel expansion transformation to a 1D grid.

    Args:
        input_grid: A list of lists or NumPy array representing the 1xN input grid.

    Returns:
        A list of lists representing the 1xN output grid after transformation.
    """
    # Convert input to NumPy array for efficient processing
    # Assuming input_grid is always a list containing one list (the row)
    # or a 2D numpy array with shape (1, N)
    input_np = np.array(input_grid, dtype=int)

    # Ensure it's a 1xN grid
    if input_np.ndim != 2 or input_np.shape[0] != 1:
        # Handle unexpected dimensions if necessary, perhaps raise error
        # For now, assume correct input format based on examples
        # If input might be 1D array directly: input_np = input_np.reshape(1, -1)
        pass # Or raise ValueError("Input must be a 1xN grid")

    input_row = input_np[0]
    height, width = input_np.shape

    # Initialize output_grid as a deep copy of the input numpy array
    # Working on a copy ensures we reference the original input for conditions
    output_np = np.copy(input_np)
    output_row = output_np[0]

    # Iterate through the pixels, checking for the isolated non-white pattern
    # We only need to check indices from 1 up to width-2 (exclusive),
    # as the pattern requires neighbors on both sides.
    for i in range(1, width - 1):
        # Get the current pixel color and its neighbors from the *original* input row
        current_pixel_color = input_row[i]
        left_neighbor_color = input_row[i-1]
        right_neighbor_color = input_row[i+1]

        # Check the condition: non-white pixel surrounded by white pixels
        if current_pixel_color > 0 and left_neighbor_color == 0 and right_neighbor_color == 0:
            # Apply the transformation to the output grid
            # Change the color of the white neighbors to the central pixel's color
            output_row[i-1] = current_pixel_color
            # output_row[i] remains current_pixel_color (already copied)
            output_row[i+1] = current_pixel_color

    # Convert the result back to a list of lists format
    output_grid = output_np.tolist()

    return output_grid