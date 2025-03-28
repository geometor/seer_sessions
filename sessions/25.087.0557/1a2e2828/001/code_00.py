import numpy as np

"""
Identify the color of the solid line (either horizontal or vertical) that spans the entire grid dimension (width for horizontal, height for vertical). The line must consist of a single non-white color. Output this color value.
"""

def transform(input_grid):
    """
    Finds the color of a solid, non-white line spanning the grid horizontally or vertically.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        int: The color value of the spanning line. Returns None if no such line is found.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    # Check for horizontal spanning lines
    for r in range(height):
        # Get the color of the first pixel in the row
        first_pixel_color = input_grid[r, 0]
        # Check if the color is non-white (not 0)
        if first_pixel_color != 0:
            # Assume this row is a spanning line initially
            is_spanning_line = True
            # Check if all other pixels in the row have the same color
            for c in range(1, width):
                if input_grid[r, c] != first_pixel_color:
                    is_spanning_line = False
                    break
            # If it is a spanning line, return its color
            if is_spanning_line:
                return first_pixel_color

    # Check for vertical spanning lines (only if no horizontal one was found)
    for c in range(width):
        # Get the color of the first pixel in the column
        first_pixel_color = input_grid[0, c]
        # Check if the color is non-white (not 0)
        if first_pixel_color != 0:
            # Assume this column is a spanning line initially
            is_spanning_line = True
            # Check if all other pixels in the column have the same color
            for r in range(1, height):
                if input_grid[r, c] != first_pixel_color:
                    is_spanning_line = False
                    break
            # If it is a spanning line, return its color
            if is_spanning_line:
                return first_pixel_color

    # Should not happen based on examples, but handle the case where no line is found
    # According to the problem description, the output should be an integer (representing the color).
    # Returning None might indicate an error or an unexpected input.
    # However, since the examples always produce a color, we expect one of the loops to return.
    # If the code reaches here, it implies an input structure not covered by the training examples.
    # For robustness, we could raise an error or return a default value, but sticking to the
    # observed pattern, we assume a line is always found.
    # For compliance with the format, we return an int, perhaps -1 to signal no line found.
    # Let's assume based on examples a line is always found and return value will be from the loops.
    # If execution reaches here, it implies a problem or unexpected input.
    # Let's return 0 (white) as a fallback, although this scenario isn't in the examples.
    return 0 # Fallback, though unlikely based on provided examples.
