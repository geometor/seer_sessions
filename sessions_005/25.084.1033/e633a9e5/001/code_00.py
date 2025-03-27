import numpy as np

"""
Transforms a 3x3 input grid into a 5x5 output grid by scaling pixels based on their position.
Edge pixels (rows 0/2, columns 0/2) are scaled 2x in the edge dimension(s).
The center pixel (row 1, column 1) is scaled 1x.
The output grid is constructed by placing these scaled blocks adjacent to each other, 
maintaining the relative order of the original input pixels.
"""

def get_vertical_scale(row_index, input_height):
    """
    Determines the vertical scaling factor for a given row index.
    Returns 2 if the row is the first or last, 1 otherwise.
    """
    if row_index == 0 or row_index == input_height - 1:
        return 2
    else:
        return 1

def get_horizontal_scale(col_index, input_width):
    """
    Determines the horizontal scaling factor for a given column index.
    Returns 2 if the column is the first or last, 1 otherwise.
    """
    if col_index == 0 or col_index == input_width - 1:
        return 2
    else:
        return 1

def transform(input_grid):
    """
    Applies position-dependent scaling to transform the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # --- Calculate output grid dimensions ---
    # Sum the vertical scale factors for each row
    output_height = sum(get_vertical_scale(r, input_height) for r in range(input_height))
    # Sum the horizontal scale factors for each column
    output_width = sum(get_horizontal_scale(c, input_width) for c in range(input_width))

    # --- Initialize output grid ---
    # Create an empty output grid with the calculated dimensions
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # --- Fill the output grid based on scaled input pixels ---
    current_out_row = 0  # Pointer for the current row position in the output grid
    # Iterate through each row of the input grid
    for r in range(input_height):
        current_out_col = 0  # Pointer for the current column position in the output grid
        # Determine the vertical scale factor for the current input row
        sv = get_vertical_scale(r, input_height)

        # Iterate through each column of the input grid
        for c in range(input_width):
            # Get the color of the current input pixel
            color = input_np[r, c]
            # Determine the horizontal scale factor for the current input column
            sh = get_horizontal_scale(c, input_width)

            # Fill the rectangular region in the output grid
            # The region starts at (current_out_row, current_out_col)
            # Its dimensions are sv (height) x sh (width)
            # All pixels in this region are set to the input pixel's color
            output_grid[current_out_row:current_out_row + sv, current_out_col:current_out_col + sh] = color

            # Move the output column pointer to the right by the horizontal scale factor
            current_out_col += sh

        # Move the output row pointer down by the vertical scale factor
        current_out_row += sv

    # Convert the final numpy array back to a list of lists for the standard ARC format
    return output_grid.tolist()