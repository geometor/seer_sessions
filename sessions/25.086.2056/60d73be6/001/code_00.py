import numpy as np

"""
Reflects non-background, non-axis pixels across a single complete line (axis) of a non-background color.

The transformation identifies a single complete horizontal or vertical line within the input grid that consists of a single, non-background color. This line acts as the axis of reflection. It then iterates through all pixels in the input grid. If a pixel is neither the background color (7) nor part of the identified axis, its position is reflected across the axis. The color of the original pixel is then placed at the calculated reflected position in the output grid. The output grid initially starts as a copy of the input grid, so original elements (including the axis and the pixels being reflected) are preserved.
"""

def find_axis(grid):
    """
    Finds a complete horizontal or vertical line of a single non-background color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: ('h', row_index) if a horizontal axis is found,
               ('v', col_index) if a vertical axis is found,
               (None, None) if no axis is found.
    """
    height, width = grid.shape
    background_color = 7

    # Check for horizontal axis
    for r in range(height):
        first_pixel_color = grid[r, 0]
        if first_pixel_color != background_color and np.all(grid[r, :] == first_pixel_color):
            return 'h', r

    # Check for vertical axis
    for c in range(width):
        first_pixel_color = grid[0, c]
        if first_pixel_color != background_color and np.all(grid[:, c] == first_pixel_color):
            return 'v', c

    return None, None # No axis found

def transform(input_grid):
    """
    Applies the reflection transformation to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np)
    background_color = 7

    # Find the axis of symmetry
    axis_type, axis_index = find_axis(input_np)

    if axis_type is None:
        # If no axis is found, return the original grid (or handle as an error/edge case)
        # Based on examples, an axis always exists.
        return input_grid # Return as list of lists

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]

            # Skip background pixels
            if color == background_color:
                continue

            # Skip pixels on the axis itself
            is_on_axis = False
            if axis_type == 'h' and r == axis_index:
                is_on_axis = True
            elif axis_type == 'v' and c == axis_index:
                is_on_axis = True

            if is_on_axis:
                continue

            # This pixel is not background and not on the axis, so reflect it
            r_reflected, c_reflected = -1, -1 # Initialize with invalid values

            if axis_type == 'h':
                # Reflect vertically across the horizontal axis
                r_reflected = 2 * axis_index - r
                c_reflected = c
            elif axis_type == 'v':
                # Reflect horizontally across the vertical axis
                r_reflected = r
                c_reflected = 2 * axis_index - c

            # Check if the reflected coordinates are within the grid bounds
            if 0 <= r_reflected < height and 0 <= c_reflected < width:
                # Apply the color to the reflected position in the output grid
                output_grid[r_reflected, c_reflected] = color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()