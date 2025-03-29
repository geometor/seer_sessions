```python
import numpy as np

"""
Reflects non-white, non-blue pixels across a blue line axis (either horizontal or vertical).
The color of the original pixel is swapped according to predefined pairs (Red<->Green, Azure<->Yellow, Gray<->Magenta).
The original color (before swapping) is placed at the reflected position.
The blue line and white background remain unchanged, except where overwritten by reflected pixels.
"""

def find_reflection_axis(grid_array):
    """
    Finds the horizontal or vertical blue line axis.

    Args:
        grid_array: A numpy array representing the grid.

    Returns:
        A tuple (orientation, index) where orientation is 'h' or 'v',
        and index is the row or column index of the line.
        Returns (None, -1) if no axis is found.
    """
    height, width = grid_array.shape

    # Check for horizontal line
    for r in range(height):
        if np.all(grid_array[r, :] == 1):
            return 'h', r

    # Check for vertical line
    for c in range(width):
        if np.all(grid_array[:, c] == 1):
            return 'v', c

    return None, -1 # Should not happen based on task constraints

def reflect_coordinates(r, c, axis_orientation, axis_index):
    """
    Calculates the reflected coordinates across the axis.

    Args:
        r: Original row index.
        c: Original column index.
        axis_orientation: 'h' for horizontal, 'v' for vertical.
        axis_index: The index of the axis line.

    Returns:
        A tuple (ref_r, ref_c) representing the reflected coordinates.
    """
    ref_r, ref_c = -1, -1
    if axis_orientation == 'h':
        # Reflect vertically across the horizontal line
        ref_r = axis_index + (axis_index - r)
        ref_c = c
    elif axis_orientation == 'v':
        # Reflect horizontally across the vertical line
        ref_r = r
        ref_c = axis_index + (axis_index - c)
    return ref_r, ref_c

def transform(input_grid):
    """
    Applies the reflection and color swap transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_array) # Initialize output as a copy
    height, width = input_array.shape

    # 1. Find the reflection axis
    line_orientation, line_index = find_reflection_axis(input_array)

    if line_orientation is None:
        # This case should ideally not be reached given the task structure
        return input_grid # Return original if no axis found

    # 2. Define the color swap mapping
    color_swap_map = {
        2: 3, 3: 2,  # Red <-> Green
        8: 4, 4: 8,  # Azure <-> Yellow
        5: 6, 6: 5   # Gray <-> Magenta
        # Other colors map to themselves (identity swap)
    }

    # 3. Iterate through each pixel to find source pixels
    for r in range(height):
        for c in range(width):
            original_color = input_array[r, c]

            # 4. Check if the pixel is a source pixel (not white and not blue)
            if original_color != 0 and original_color != 1:

                # 5a. Calculate reflection coordinates
                ref_r, ref_c = reflect_coordinates(r, c, line_orientation, line_index)

                # 5b. Determine the swapped color
                swapped_color = color_swap_map.get(original_color, original_color) # Default to original if not in map

                # 5c. Update the output grid
                # Place the swapped color at the original position
                output_grid[r, c] = swapped_color

                # Place the original color at the reflected position, checking bounds
                if 0 <= ref_r < height and 0 <= ref_c < width:
                    output_grid[ref_r, ref_c] = original_color

    # Convert the numpy array back to a list of lists before returning
    return output_grid.tolist()
```