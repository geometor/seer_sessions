"""
Divides the input grid into four quadrants, determines an expanding and fill color for each quadrant within each example, transforms each quadrant by expanding the expanding color and filling the rest with the fill color, and then combines the transformed quadrants into an output grid. The output grid's dimensions are calculated as (input_rows + 1) // 2 and (input_cols + 1) // 2.
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

def determine_colors(input_quadrant, output_quadrant):
    # Find unique colors in the input quadrant
    input_colors = np.unique(input_quadrant)

    # Find unique colors in the output quadrant
    output_colors = np.unique(output_quadrant)

    # Expanding color is present in input
    expanding_color = input_colors[0]  # Initialize
    for color in input_colors:
        if np.any(input_quadrant == color):
             expanding_color = color
             break

    # Find the fill color present in the output but not matching expanding
    fill_color = output_colors[0]
    for color in output_colors:
        if color != expanding_color:
            fill_color = color
            break

    return expanding_color, fill_color

def transform_quadrant(quadrant, expanding_color, fill_color):
    rows, cols = quadrant.shape
    new_quadrant = np.full((rows, cols), fill_color, dtype=int) # Initialize with fill color

    for r in range(rows):
        for c in range(cols):
            if quadrant[r, c] == expanding_color:
                new_quadrant[r, c] = expanding_color

    return new_quadrant

def transform(input_grid, output_grid_for_color_det):
    # Calculate output dimensions
    input_rows, input_cols = input_grid.shape
    output_rows = (input_rows + 1) // 2
    output_cols = (input_cols + 1) // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Divide the input grid into four quadrants
    quadrant_names = ["top_left", "top_right", "bottom_left", "bottom_right"]
    input_quadrants = {}
    output_quadrants = {} # For color determination
    for q_name in quadrant_names:
        input_quadrants[q_name] = get_quadrant(input_grid, q_name)
        output_quadrants[q_name] = get_quadrant(output_grid_for_color_det, q_name)

    # Transform each quadrant
    transformed_quadrants = {}
    for q_name in quadrant_names:
        expanding_color, fill_color = determine_colors(input_quadrants[q_name], output_quadrants[q_name])
        transformed_quadrants[q_name] = transform_quadrant(input_quadrants[q_name], expanding_color, fill_color)


    # Combine the quadrants to form the output grid
    output_grid[:input_quadrants["top_left"].shape[0], :input_quadrants["top_left"].shape[1]] = transformed_quadrants["top_left"]
    output_grid[:input_quadrants["top_right"].shape[0], input_quadrants["top_left"].shape[1]:] = transformed_quadrants["top_right"]
    output_grid[input_quadrants["top_left"].shape[0]:, :input_quadrants["bottom_left"].shape[1]] = transformed_quadrants["bottom_left"]
    output_grid[input_quadrants["top_right"].shape[0]:, input_quadrants["bottom_left"].shape[1]:] = transformed_quadrants["bottom_right"]

    return output_grid