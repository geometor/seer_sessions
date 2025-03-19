"""
The transformation rule involves identifying an azure pixel (value 8) in the input grid and generating an "L"-shaped path of gray pixels (value 5) originating from the azure pixel's location. The "L" shape can have variable length/orientation. We need to determine a general rule for the L shape's orientation and dimensions.
"""

import numpy as np

def find_azure_pixel(grid):
    # Find the coordinates of the azure pixel (value 8).
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 8:
                return (r, c)
    return None  # Should not happen, based on task description.

def determine_l_shape(azure_pos):
    # Placeholder for a function that will determine the L-shape's
    # orientation and dimensions based on the azure pixel's position.
    # Currently, this function returns hardcoded values, and needs to
    # be generalized based on further analysis of the examples.
    r, c = azure_pos

    # Dummy logic for testing.  This needs to be a general rule.
    if r > 2 and c > 2:
        return "up-left", 3, 2  # direction, length1, length2
    elif r < 10 and c > 2:
        return "down-left", 3, 2
    elif r < 10 and c < 10:
        return "down-right", 3, 2
    elif r > 2 and c < 10:
        return "up-right", 3, 2


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the azure pixel.
    azure_pos = find_azure_pixel(input_grid)

    if azure_pos is None:
        return output_grid # Should not happen

    # Determine L-shape parameters.
    direction, length1, length2 = determine_l_shape(azure_pos)

    # Draw the L-shape based on the determined parameters.
    r, c = azure_pos

    if direction == "up-left":
        for i in range(1, length1 + 1):
            output_grid[r - i, c] = 5
        for i in range(1, length2 + 1):
            output_grid[r - length1, c - i] = 5
    elif direction == "down-left":
        for i in range(1, length1 + 1):
            output_grid[r + i, c] = 5
        for i in range(1, length2 + 1):
            output_grid[r + length1, c - i] = 5
    elif direction == "down-right":
        for i in range(1, length1 + 1):
            output_grid[r + i, c] = 5
        for i in range(1, length2 + 1):
            output_grid[r + length1, c + i] = 5
    elif direction == "up-right":
        for i in range(1, length1 + 1):
            output_grid[r - i, c] = 5
        for i in range(1, length2 + 1):
            output_grid[r - length1, c + i] = 5

    return output_grid