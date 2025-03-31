```python
import numpy as np

"""
The transformation identifies a primary axis line (horizontal or vertical) composed 
of blue (1) and white (0) pixels, selecting the one with the most blue pixels. 
It then reflects all non-white, non-axis pixels across this line, swapping 
their colors according to specific pairs: Azure(8) <-> Yellow(4), 
Red(2) <-> Green(3), Gray(5) <-> Magenta(6). The axis line itself (only the 
blue pixels) is preserved in the output.
"""

# Define the color swapping pairs
COLOR_SWAP_MAP = {
    8: 4,  # Azure -> Yellow
    4: 8,  # Yellow -> Azure
    2: 3,  # Red -> Green
    3: 2,  # Green -> Red
    5: 6,  # Gray -> Magenta
    6: 5,  # Magenta -> Gray
    # Identity mappings for other colors (including background and axis color)
    0: 0,
    1: 1,
    7: 7,
    9: 9
}

def find_reflection_axis(grid):
    """
    Finds the reflection axis (a line of blue(1) and white(0) pixels).
    Selects the axis (horizontal or vertical) with the maximum number of blue pixels.
    """
    height, width = grid.shape
    best_axis_type = None
    best_axis_idx = -1
    max_blue_count = 0

    # Check horizontal candidates
    for r in range(height):
        is_potential_axis = True
        blue_count = 0
        for c in range(width):
            pixel = grid[r, c]
            if pixel == 1:
                blue_count += 1
            elif pixel != 0: # Must be only 0s and 1s
                is_potential_axis = False
                break
        if is_potential_axis and blue_count > 0:
            if blue_count > max_blue_count:
                 max_blue_count = blue_count
                 best_axis_type = 'horizontal'
                 best_axis_idx = r
            # Simple tie-breaking: prefer horizontal if counts are equal
            elif blue_count == max_blue_count and best_axis_type == 'vertical':
                 best_axis_type = 'horizontal'
                 best_axis_idx = r


    # Check vertical candidates
    for c in range(width):
        is_potential_axis = True
        blue_count = 0
        for r in range(height):
             pixel = grid[r, c]
             if pixel == 1:
                 blue_count += 1
             elif pixel != 0: # Must be only 0s and 1s
                is_potential_axis = False
                break
        if is_potential_axis and blue_count > 0:
             if blue_count > max_blue_count:
                 max_blue_count = blue_count
                 best_axis_type = 'vertical'
                 best_axis_idx = c
             # Tie-breaking already handled (prefer horizontal if equal)

    return best_axis_type, best_axis_idx


def transform(input_grid):
    """
    Applies the reflection and color swap transformation based on the identified axis.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # initialize output_grid with background color (white, 0)
    output_np = np.zeros_like(input_np)

    # Find the axis of reflection
    axis_type, axis_idx = find_reflection_axis(input_np)

    if axis_type is None:
        # No axis found - return the input grid or an empty grid?
        # Based on examples, an axis should always be present.
        # Returning input might be safer for unexpected cases.
        print("Warning: No reflection axis found.")
        return input_grid

    # Copy the blue pixels from the axis line to the output grid
    if axis_type == 'horizontal':
        for c in range(width):
            if input_np[axis_idx, c] == 1:
                output_np[axis_idx, c] = 1
    elif axis_type == 'vertical':
        for r in range(height):
            if input_np[r, axis_idx] == 1:
                output_np[r, axis_idx] = 1

    # Iterate through each pixel of the input grid to reflect and swap
    for r in range(height):
        for c in range(width):
            original_color = input_np[r, c]

            # Skip background color (0)
            if original_color == 0:
                continue

            # Skip pixels on the axis line itself
            if axis_type == 'horizontal' and r == axis_idx:
                continue
            if axis_type == 'vertical' and c == axis_idx:
                continue

            # Calculate reflected position
            reflected_r, reflected_c = r, c # Initialize
            if axis_type == 'horizontal':
                reflected_r = (2 * axis_idx) - r
            elif axis_type == 'vertical':
                reflected_c = (2 * axis_idx) - c

            # Check if the reflected position is within grid bounds
            if 0 <= reflected_r < height and 0 <= reflected_c < width:
                # Get the swapped color
                swapped_color = COLOR_SWAP_MAP.get(original_color, original_color)

                # Place the swapped color at the reflected position in the output grid
                output_np[reflected_r, reflected_c] = swapped_color

    # Convert back to list of lists for the expected output format
    return output_np.tolist()
```