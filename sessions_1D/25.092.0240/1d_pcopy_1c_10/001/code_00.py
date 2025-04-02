"""
Transformation Rule:
Iterate through the input row. If a non-white pixel is found that is "isolated" 
(meaning its immediate left and right neighbors are white, or it's at an edge 
adjacent to white), expand this pixel into a horizontal block of three pixels 
of the same color in the output row, overwriting the original position and its 
neighbors. Pixels that are not isolated non-white pixels (including white pixels 
and non-white pixels already part of a block) are copied directly from input to output.
"""

import numpy as np

def is_isolated(grid_row, index, width):
    """
    Checks if a non-white pixel at a given index is isolated.

    Args:
        grid_row: The 1D numpy array representing the row.
        index: The index of the pixel to check.
        width: The total width of the row.

    Returns:
        True if the pixel is non-white and isolated, False otherwise.
    """
    # Check if the pixel itself is non-white (not 0)
    if grid_row[index] == 0:
        return False

    # Check left neighbor
    left_is_white = (index == 0) or (grid_row[index - 1] == 0)

    # Check right neighbor
    right_is_white = (index == width - 1) or (grid_row[index + 1] == 0)

    # It's isolated if both neighbors are white (or it's at an edge next to white)
    return left_is_white and right_is_white

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Expand isolated non-white pixels into 3-pixel blocks.

    Args:
        input_grid: A list containing a single list (representing the 1D row).

    Returns:
        A list containing a single list (the transformed 1D row).
    """
    # Ensure input is treated as a numpy array for easier handling
    # The input format seems to be list of lists, even for 1D
    input_row = np.array(input_grid[0], dtype=int)
    width = len(input_row)

    # Create a copy of the input row to modify for the output
    # This handles copying pixels that are not part of an expansion
    output_row = np.copy(input_row)

    # Iterate through each pixel in the input row
    for i in range(width):
        # Check if the pixel at index i in the *original* input is isolated
        if is_isolated(input_row, i, width):
            # Get the color of the isolated pixel
            color = input_row[i]

            # Apply the expansion to the output row
            # Set the center pixel (current index i)
            output_row[i] = color

            # Set the left neighbor if it exists
            if i > 0:
                output_row[i - 1] = color

            # Set the right neighbor if it exists
            if i < width - 1:
                output_row[i + 1] = color

    # Return the result in the original list-of-lists format
    return [output_row.tolist()]