```python
"""
Divide the input grid into four quadrants.  For each quadrant, a specific color expands, and all other colors are replaced with a quadrant-specific fill color. The output grid's dimensions are calculated as floor(input rows / 2) + input rows % 2 and floor(input cols / 2) + input cols % 2. The transformed quadrants are then combined to create the final output.
"""

import numpy as np

def get_quadrant(grid, quadrant_name):
    rows, cols = grid.shape
    mid_row = rows // 2
    mid_col = cols // 2

    if quadrant_name == "top_left":
        return grid[:mid_row, :mid_col]
    elif quadrant_name == "top_right":
        return grid[:mid_row, mid_col:]
    elif quadrant_name == "bottom_left":
        return grid[mid_row:, :mid_col]
    elif quadrant_name == "bottom_right":
        return grid[mid_row:, mid_col:]
    else:
        raise ValueError("Invalid quadrant name")

def transform_quadrant(quadrant, quadrant_name):
    rows, cols = quadrant.shape
    new_quadrant = np.zeros((rows, cols), dtype=int)

    if quadrant_name == "top_left":
        expanding_color = 4  # Example 2.  In ex 1, this would be 1.
        fill_color = 9 # Example 2.  In ex 1, this would be 2.

    elif quadrant_name == "top_right":
        expanding_color = 3
        fill_color = 7

    elif quadrant_name == "bottom_left":
        expanding_color = 8
        fill_color = 1

    elif quadrant_name == "bottom_right":
        expanding_color = 5
        fill_color = 1

    for r in range(rows):
        for c in range(cols):
            if quadrant[r, c] == expanding_color:
                new_quadrant[r, c] = expanding_color
            else:
                new_quadrant[r, c] = fill_color

    return new_quadrant

def transform(input_grid):
    # Calculate output dimensions
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows // 2 + input_rows % 2
    output_cols = input_cols // 2 + input_cols % 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Divide the input grid into four quadrants
    quadrant_names = ["top_left", "top_right", "bottom_left", "bottom_right"]
    quadrants = {}
    for q_name in quadrant_names:
        quadrants[q_name] = get_quadrant(input_grid, q_name)

    # Transform each quadrant
    transformed_quadrants = {}
    for q_name in quadrant_names:
        transformed_quadrants[q_name] = transform_quadrant(quadrants[q_name], q_name)


    # Combine the quadrants to form the output grid
    output_grid[:quadrants["top_left"].shape[0], :quadrants["top_left"].shape[1]] = transformed_quadrants["top_left"]
    output_grid[:quadrants["top_right"].shape[0], quadrants["top_left"].shape[1]:] = transformed_quadrants["top_right"]
    output_grid[quadrants["top_left"].shape[0]:, :quadrants["bottom_left"].shape[1]] = transformed_quadrants["bottom_left"]
    output_grid[quadrants["top_right"].shape[0]:, quadrants["bottom_left"].shape[1]:] = transformed_quadrants["bottom_right"]

    return output_grid
```