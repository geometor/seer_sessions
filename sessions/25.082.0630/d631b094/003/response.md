```python
"""
The transformation identifies the color of the single connected object and creates a new grid. The output dimensions are determined by the number of rows and columns with colored pixels from the object, and this grid is filled with the color of the object.
"""

import numpy as np

def _find_object_color(input_grid):
    # Find the non-zero color in the input
    input_array = np.array(input_grid)
    non_zero_pixels = input_array[input_array != 0]
    return non_zero_pixels[0] if non_zero_pixels.size > 0 else 0

def _count_rows_cols_with_color(input_grid, color):
    input_array = np.array(input_grid)
    rows_with_color = 0
    cols_with_color = 0

    for i in range(input_array.shape[0]):
        if color in input_array[i, :]:
            rows_with_color += 1

    for j in range(input_array.shape[1]):
        if color in input_array[:, j]:
            cols_with_color += 1

    return rows_with_color, cols_with_color
    

def transform(input_grid):
    # Find the object color.
    object_color = _find_object_color(input_grid)

    # If no object is found, return an empty grid.
    if object_color == 0:
        return []

    # Determine output dimensions.
    rows_with_color, cols_with_color = _count_rows_cols_with_color(input_grid, object_color)

    # Construct output grid.
    output_grid = np.full((rows_with_color, cols_with_color), object_color)

    return output_grid.tolist()
```