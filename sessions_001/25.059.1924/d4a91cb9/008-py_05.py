"""
Locate the azure (8) and red (2) pixels. Draw a vertical yellow (4) line from the azure pixel to the row of the red pixel. Then, draw a horizontal yellow (4) line from the end of the vertical line to the red pixel. Preserve the azure and red pixels.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the refined rule."""
    output_grid = np.copy(input_grid)
    azure_pos = find_pixel(input_grid, 8)
    red_pos = find_pixel(input_grid, 2)

    if azure_pos is None or red_pos is None:
        return output_grid

    # Vertical Segment
    if azure_pos[0] < red_pos[0]:  # Azure above Red
        for r in range(azure_pos[0] + 1, red_pos[0]):
            output_grid[r, azure_pos[1]] = 4
    elif azure_pos[0] > red_pos[0]:  # Azure below Red
        for r in range(red_pos[0] + 1, azure_pos[0]):
            output_grid[r, azure_pos[1]] = 4
    # else: Same row, no vertical line

    # Horizontal Segment
    if azure_pos[1] < red_pos[1]:  # Azure left of Red
        for c in range(azure_pos[1] + 1, red_pos[1]):
            output_grid[red_pos[0], c] = 4
    elif azure_pos[1] > red_pos[1]:  # Azure right of Red
        for c in range(red_pos[1] + 1, azure_pos[1]):
            output_grid[red_pos[0], c] = 4
    # else: Same column, no horizontal line

    return output_grid