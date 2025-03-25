"""
Transforms a grid of 0s and 5s into a grid where the 5s are replaced by a color determined by their column index,
cycling through a predefined list of colors for each column. 0s remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Define the color mapping for '5' based on column index.
    color_map = {
        0: [4, 2, 6],
        1: [0],
        2: [2, 6, 1],
        3: [0],
        4: [1, 4, 6]
    }
    
    # we only need to keep state across invocations of transform, so set it up here.
    if not hasattr(transform, 'color_index'):
        transform.color_index = 0


    # Iterate through each cell of the input grid.
    for row in range(height):
        for col in range(width):
            if input_grid[row, col] == 0:
                output_grid[row, col] = 0  # Keep 0s unchanged.
            elif input_grid[row, col] == 5:
                # Get the replacement color from the color map.
                replacement_colors = color_map.get(col)
                if replacement_colors:  # Ensure not None
                    output_grid[row, col] = replacement_colors[transform.color_index % len(replacement_colors)]

    transform.color_index += 1

    return output_grid.tolist()