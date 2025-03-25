"""
The transformation rule is a color swap. For each input-output example pair, a specific color mapping is determined. Each color in the input grid is mapped to a corresponding color in the output grid. This mapping is applied to the entire input grid to generate the output grid. The color mapping can differ between examples, but within each example, the mapping is consistent.
"""

import numpy as np

def get_color_mapping(input_grid, output_grid):
    """
    Generates a color mapping dictionary based on the input and output grids.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    unique_input_colors = np.unique(input_grid)
    color_mapping = {}
    for color in unique_input_colors:
        indices = np.where(input_grid == color)
        if indices[0].size > 0:
            output_color = output_grid[indices[0][0], indices[1][0]]
            color_mapping[color] = output_color
    return color_mapping

def transform(input_grid, output_grid):
    # Convert input and output to numpy arrays
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    # Get the color mapping
    color_mapping = get_color_mapping(input_grid.tolist(), output_grid.tolist())

    # Initialize the output grid as a copy of the input grid
    transformed_grid = np.copy(input_grid)

    # Apply the color mapping
    for old_color, new_color in color_mapping.items():
        transformed_grid[input_grid == old_color] = new_color

    return transformed_grid.tolist()