import numpy as np

"""
Transforms the input grid by applying a row-dependent horizontal shift to the pixels of the single non-white object.

1.  Create a new output grid of the same dimensions as the input, filled with white (0).
2.  Identify all non-white pixels in the input grid, which constitute the single object.
3.  Find the row index of the topmost pixel of this object (`object_top_row`).
4.  For each non-white pixel at input coordinates (row, col) with color `c`:
    a.  Calculate its relative row index: `relative_row = row - object_top_row`.
    b.  Determine the horizontal shift based on `relative_row % 4`:
        - shift 0 if `relative_row % 4` is 0 or 2.
        - shift -1 (left) if `relative_row % 4` is 1.
        - shift +1 (right) if `relative_row % 4` is 3.
    c.  Calculate the target column: `new_col = col + shift`.
    d.  If `new_col` is within the grid's horizontal boundaries, set the pixel at (row, new_col) in the output grid to the object's color `c`.
5.  Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a row-dependent horizontal shift to the non-white object in the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to a NumPy array for efficient operations
    inp = np.array(input_grid, dtype=int)
    height, width = inp.shape

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(inp)

    # Find the coordinates of all non-white pixels (the object)
    object_pixels_r, object_pixels_c = np.where(inp > 0)

    # If there's no object, return the empty grid
    if object_pixels_r.size == 0:
        return output_grid.tolist()

    # Find the topmost row of the object
    object_top_row = np.min(object_pixels_r)

    # Iterate through each pixel of the object
    for r, c in zip(object_pixels_r, object_pixels_c):
        # Get the color of the current pixel
        color = inp[r, c]

        # Calculate the row index relative to the object's top
        relative_row = r - object_top_row

        # Determine the shift amount based on the relative row index modulo 4
        shift_index = relative_row % 4
        if shift_index == 1:
            shift_amount = -1  # Shift left
        elif shift_index == 3:
            shift_amount = 1   # Shift right
        else:  # shift_index is 0 or 2
            shift_amount = 0   # No shift

        # Calculate the new column position
        new_c = c + shift_amount

        # Check if the new column is within the grid boundaries
        if 0 <= new_c < width:
            # Place the pixel's color at the new position in the output grid
            output_grid[r, new_c] = color

    # Convert the NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()