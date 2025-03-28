import numpy as np

"""
Transforms an input grid by replacing each non-white (non-zero) pixel 
with a 3x3 square in the output grid. The center of the square retains 
the original pixel's color, and the surrounding 8 border pixels of the 
square adopt a new color based on a specific mapping:
- green (3) center -> magenta (6) border
- red (2) center -> blue (1) border
- azure (8) center -> yellow (4) border
The output grid has the same dimensions as the input grid and retains a 
white (0) background otherwise. Non-white input pixels whose colors are not 
in the mapping are ignored.
"""

def transform(input_grid):
    """
    Applies the 3x3 expansion and color mapping transformation.

    Args:
        input_grid (list of lists): A 2D grid represented as a list of lists
                                      of integers (0-9).

    Returns:
        list of lists: The transformed 2D grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    # Using numpy allows for efficient array operations and indexing.
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize the output grid with the background color (white/0).
    # Using np.zeros_like ensures the output has the same shape and dtype
    # as the input, filled initially with zeros.
    output_np = np.zeros_like(input_np)

    # Define the color mapping for the border based on the center color.
    # This mapping is derived directly from the provided training examples.
    color_map_border = {
        3: 6,  # green center -> magenta border
        2: 1,  # red center -> blue border
        8: 4   # azure center -> yellow border
    }

    # Iterate through each pixel (cell) of the input grid using its row and column index.
    for r in range(rows):
        for c in range(cols):
            # Get the color of the current pixel in the input grid.
            center_color = input_np[r, c]

            # Check if the pixel is non-white (color value is not 0).
            # These are the pixels that trigger the transformation.
            if center_color != 0:
                # Determine the corresponding border color using the predefined map.
                # .get() safely retrieves the value, returning None if the key (center_color) doesn't exist.
                border_color = color_map_border.get(center_color)

                # Proceed only if a valid mapping exists for the current center color.
                # If border_color is None, it means the input pixel's color is not one of {2, 3, 8},
                # and according to the examples, such pixels should be ignored (left as 0 in output).
                if border_color is not None:
                    # Iterate through the 3x3 neighborhood centered at the current pixel (r, c).
                    # dr represents the row offset from the center (-1, 0, or 1).
                    # dc represents the column offset from the center (-1, 0, or 1).
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            # Calculate the coordinates (nr, nc) of the neighbor pixel in the grid.
                            nr, nc = r + dr, c + dc

                            # Crucially, check if the calculated neighbor coordinates are within
                            # the valid boundaries of the grid (0 <= row < rows, 0 <= col < cols).
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # If the offsets are both 0, this is the center pixel of the 3x3 square.
                                if dr == 0 and dc == 0:
                                    # Set the center pixel in the output grid to the original input color.
                                    output_np[nr, nc] = center_color
                                # Otherwise, it's one of the 8 border pixels of the 3x3 square.
                                else:
                                    # Set the border pixel in the output grid to the mapped border color.
                                    output_np[nr, nc] = border_color

    # Convert the resulting numpy array back to a standard Python list of lists
    # format, as required by the ARC environment.
    output_grid = output_np.tolist()
    return output_grid