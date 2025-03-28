import numpy as np

"""
Reflects non-background, non-axis pixels across a single, complete line (axis) of a non-background color. The output grid starts as a copy of the input, and the reflected pixels are added (overwriting) at their corresponding reflected locations.

The transformation identifies a single complete horizontal or vertical line (axis) within the input grid that consists of a single, non-background color. This line acts as the axis of reflection. The background color is identified as orange (7). The output grid is initialized as an exact copy of the input grid. The transformation then iterates through all pixels in the input grid. If a pixel's color is not the background color (7) and the pixel is not located on the identified axis, its position is mathematically reflected across the axis. If the calculated reflected position is within the grid bounds, the color of the original pixel is placed at that reflected position in the output grid, overwriting whatever color was previously there (including background pixels or pixels from the initial copy). Pixels on the axis, background pixels, and the original non-background/non-axis pixels remain as they were in the initial copy. Pixels whose reflections fall outside the grid bounds are ignored.
"""

def find_axis(grid, background_color):
    """
    Finds a complete horizontal or vertical line of a single non-background color.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The integer value representing the background color.

    Returns:
        tuple: ('h', row_index) if a horizontal axis is found,
               ('v', col_index) if a vertical axis is found,
               (None, None) if no axis is found.
    """
    height, width = grid.shape

    # Check for horizontal axis
    for r in range(height):
        first_pixel_color = grid[r, 0]
        # Check if the first pixel is not background and the entire row has the same color
        if first_pixel_color != background_color and np.all(grid[r, :] == first_pixel_color):
            # Ensure it's a complete line
            if grid[r, :].size == width:
                 return 'h', r

    # Check for vertical axis
    for c in range(width):
        first_pixel_color = grid[0, c]
        # Check if the first pixel is not background and the entire column has the same color
        if first_pixel_color != background_color and np.all(grid[:, c] == first_pixel_color):
             # Ensure it's a complete line
             if grid[:, c].size == height:
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
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # Define background color
    background_color = 7

    # Find the axis of symmetry using the helper function
    axis_type, axis_index = find_axis(input_np, background_color)

    # If no axis is found (as a safeguard, though examples imply one always exists)
    if axis_type is None:
        return input_grid # Return original grid as list of lists

    # Iterate through each pixel of the *input* grid
    for r in range(height):
        for c in range(width):
            # Get the color from the original input grid
            color = input_np[r, c]

            # 1. Skip background pixels
            if color == background_color:
                continue

            # 2. Determine if the current pixel is on the axis
            is_on_axis = False
            if axis_type == 'h' and r == axis_index:
                is_on_axis = True
            elif axis_type == 'v' and c == axis_index:
                is_on_axis = True

            # 3. Skip pixels on the axis itself
            if is_on_axis:
                continue

            # 4. If pixel is not background and not on axis, calculate its reflection
            r_reflected, c_reflected = -1, -1 # Initialize with invalid values

            if axis_type == 'h':
                # Reflect vertically across the horizontal axis
                r_reflected = 2 * axis_index - r
                c_reflected = c
            elif axis_type == 'v':
                # Reflect horizontally across the vertical axis
                r_reflected = r
                c_reflected = 2 * axis_index - c

            # 5. Check if the reflected coordinates are within the grid bounds
            if 0 <= r_reflected < height and 0 <= c_reflected < width:
                # 6. Update the *output grid* at the reflected position
                #    with the original pixel's color. This overwrites the
                #    destination cell in the output grid.
                output_grid[r_reflected, c_reflected] = color
            # Else: If reflection is outside bounds, do nothing.

    # Convert the final numpy array back to list of lists for the expected output format
    return output_grid.tolist()