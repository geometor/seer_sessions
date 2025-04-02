import numpy as np

"""
Fill segments of white (0) pixels that are located between two pixels of the 
same non-white color. The fill color used is the color of the bounding non-white pixels.
The transformation operates on a single row (1D grid). Pixels not part of such 
a fillable segment remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by filling white segments between identical non-white pixels.

    Args:
        input_grid: A numpy array representing the input grid (expected to be 1D or have one dimension of size 1).

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Ensure we're working with a 1D array
    # Flatten the input in case it's 1xN or Nx1
    input_row = input_grid.flatten()
    
    # Initialize the output grid as a copy of the input row
    output_row = np.copy(input_row)
    
    # Variables to track the last seen non-white pixel
    last_non_white_idx = -1
    last_non_white_color = -1 # Use -1 to indicate no color seen yet

    # Iterate through the input row
    for i, current_color in enumerate(input_row):
        # Check if the current pixel is non-white (not 0)
        if current_color != 0:
            # Check if we have seen a previous non-white pixel 
            # AND if the current non-white color matches the last seen non-white color
            if last_non_white_idx != -1 and current_color == last_non_white_color:
                # Fill the gap between the last non-white pixel and the current one
                # The range goes from the index *after* the last non-white pixel
                # up to (but not including) the current index 'i'.
                for fill_idx in range(last_non_white_idx + 1, i):
                    # Only fill if the pixel is currently white (though the examples suggest they always are)
                    if output_row[fill_idx] == 0:
                       output_row[fill_idx] = current_color

            # Update the tracking variables for the current non-white pixel
            last_non_white_idx = i
            last_non_white_color = current_color

    # Reshape the output row back to the original input grid shape
    output_grid = output_row.reshape(input_grid.shape)

    return output_grid