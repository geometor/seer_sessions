```python
"""
Transformation rule:
1. Initialize the output grid as a copy of the input grid, filled entirely with the background color ('white', 0).
2. Locate the 'marker' pixel (color 'magenta', 6) in the input grid and record its position (index).
3. Place the 'marker' pixel into the output grid at the same recorded position.
4. Identify the contiguous block of pixels in the input grid whose color is neither 'white' (0) nor 'magenta' (6). This is the 'movable object'. Record its color and length.
5. Determine the target end position for the 'movable object' in the output grid: it should be the position immediately to the left of the 'marker' pixel (marker index - 1).
6. Determine the target start position for the 'movable object': target end position - length + 1.
7. Place the 'movable object' (using its recorded color and length) into the output grid starting at the calculated target start position.
8. Return the modified output grid.
"""

import numpy as np

def find_marker(grid_row):
    """Finds the index of the marker pixel (color 6)."""
    for idx, pixel in enumerate(grid_row):
        if pixel == 6:
            return idx
    return -1 # Should not happen based on examples

def find_movable_object(grid_row):
    """Finds the color, start index, end index, and length of the movable object."""
    start_index = -1
    end_index = -1
    object_color = -1
    length = 0
    for idx, pixel in enumerate(grid_row):
        if pixel != 0 and pixel != 6:
            if start_index == -1:
                start_index = idx
                object_color = pixel
            end_index = idx
            length += 1
        elif start_index != -1: # Found the end of the object
             break # Optimization since object is contiguous
    return object_color, start_index, end_index, length

def transform(input_grid):
    """
    Transforms the input grid by moving the contiguous colored block (non-white, non-magenta)
    so its right edge is adjacent to the left of the magenta marker pixel.
    """
    # Since the examples are 1D, we handle the first row.
    # Convert to numpy array for easier slicing if needed, though list operations are sufficient here.
    # Assuming input_grid is a list of lists, even if only one inner list.
    input_row = input_grid[0]
    grid_width = len(input_row)

    # 1. Initialize the output grid filled with background color (0)
    output_row = [0] * grid_width

    # 2. Locate the marker pixel (6) and record its position
    marker_index = find_marker(input_row)
    if marker_index == -1:
        # Handle error case or return input if marker not found?
        # Based on examples, marker is always present.
        return input_grid # Or raise an error

    # 3. Place the marker pixel into the output grid
    output_row[marker_index] = 6

    # 4. Identify the movable object (color != 0 and != 6) and record its color and length
    object_color, _, _, object_length = find_movable_object(input_row)
    if object_color == -1:
         # Handle error case or return input if object not found?
         # Based on examples, object is always present.
         return input_grid # Or raise an error

    # 5. Determine the target end position for the movable object
    target_end_index = marker_index - 1

    # 6. Determine the target start position for the movable object
    target_start_index = target_end_index - object_length + 1

    # 7. Place the movable object into the output grid
    for i in range(object_length):
        if 0 <= target_start_index + i < grid_width: # Boundary check
            output_row[target_start_index + i] = object_color

    # Return the modified output grid (as a list of lists)
    return [output_row]

```