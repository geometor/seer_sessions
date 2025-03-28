```python
import numpy as np

"""
Reflects non-background, non-axis pixels across a single complete line (axis) of a non-background color, but only onto positions that are currently background color.

The transformation identifies a single complete horizontal or vertical line (axis) within the input grid that consists of a single, non-background color. This line acts as the axis of reflection. The background color is identified as orange (7). The output grid is initialized as a copy of the input grid. The transformation then iterates through all pixels in the input grid. If a pixel's color is not the background color (7) and the pixel is not located on the identified axis, its position is mathematically reflected across the axis. If the calculated reflected position in the output grid currently contains the background color (7), the color of the original pixel is placed at that reflected position. If the reflected position already contains a non-background color (due to being part of the original input or a previously reflected pixel), it remains unchanged by the current reflection operation. Pixels on the axis and background pixels are not reflected and remain as they were in the initial copy.
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
            # Verify it's a complete line (no background color interruptions)
            # np.all already ensures this
            return 'h', r

    # Check for vertical axis
    for c in range(width):
        first_pixel_color = grid[0, c]
        # Check if the first pixel is not background and the entire column has the same color
        if first_pixel_color != background_color and np.all(grid[:, c] == first_pixel_color):
             # Verify it's a complete line (no background color interruptions)
             # np.all already ensures this
            return 'v', c

    return None, None # No axis found

def transform(input_grid):
    """
    Applies the conditional reflection transformation to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    # Define background color
    background_color = 7

    # Find the axis of symmetry
    axis_type, axis_index = find_axis(input_np, background_color)

    # If no axis is found, return the original grid (based on examples, an axis always exists)
    if axis_type is None:
        return input_grid # Return as list of lists

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]

            # Skip background pixels
            if color == background_color:
                continue

            # Determine if the current pixel is on the axis
            is_on_axis = False
            if axis_type == 'h' and r == axis_index:
                is_on_axis = True
            elif axis_type == 'v' and c == axis_index:
                is_on_axis = True

            # Skip pixels on the axis itself
            if is_on_axis:
                continue

            # This pixel is not background and not on the axis, calculate its reflection
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
                # Check if the target cell in the output grid is currently background color
                if output_grid[r_reflected, c_reflected] == background_color:
                    # Apply the original pixel's color to the reflected position
                    output_grid[r_reflected, c_reflected] = color
                # Else: If the target cell is not background, do nothing (preserve existing content)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```