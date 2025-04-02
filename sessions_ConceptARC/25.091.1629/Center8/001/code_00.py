"""
Identifies horizontal line segments in the input grid. For each horizontal line, it checks if there is a non-white 'marker' pixel directly above the starting pixel of the line. If a marker pixel exists, a 3-pixel high vertical line is drawn in the output grid. This vertical line uses the color of the marker pixel and is centered horizontally at the midpoint of the original horizontal line, and vertically centered on the row of the original horizontal line. All other pixels from the input are preserved unless overwritten by the new vertical line.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Iterate through each pixel to find potential starts of horizontal lines
    for r in range(height):
        for c in range(width):
            # Check if this pixel is the start of a horizontal line
            # Condition: Pixel is not white AND (it's the first column OR the pixel to the left is white)
            is_start_of_line = input_array[r, c] != 0 and (c == 0 or input_array[r, c-1] == 0)

            if is_start_of_line:
                line_color = input_array[r, c]
                start_col = c
                end_col = start_col

                # Find the end of the horizontal line
                while end_col + 1 < width and input_array[r, end_col + 1] == line_color:
                    end_col += 1

                # Check for the marker pixel above the start of the line
                marker_color = 0 # Default to white (no marker)
                if r > 0: # Ensure we are not on the top row
                    potential_marker_color = input_array[r - 1, start_col]
                    if potential_marker_color != 0: # Check if marker is not white
                        marker_color = potential_marker_color

                # If a valid marker was found, draw the vertical line
                if marker_color != 0:
                    # Calculate the midpoint column
                    mid_col = (start_col + end_col) // 2

                    # Draw the 3-pixel vertical line in the output grid
                    # Pixel above the line's row
                    if r - 1 >= 0:
                         output_array[r - 1, mid_col] = marker_color
                    # Pixel on the line's row (overwriting part of the original line)
                    output_array[r, mid_col] = marker_color
                    # Pixel below the line's row
                    if r + 1 < height:
                         output_array[r + 1, mid_col] = marker_color

    # Convert the output numpy array back to a list of lists
    return output_array.tolist()