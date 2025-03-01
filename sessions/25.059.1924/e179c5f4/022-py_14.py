"""
1.  **Identify Existing Lines:** Find existing horizontal and vertical lines in the input grid. A line is defined as a row or column where there's more than one color and *at least one* color is not the background (8/azure or 0/white).
2.  **Find Intersection:** Determine the intersection point (x, y) of these lines.  If there are no existing lines, there is no transformation, and the output is identical to the input.
3.  **Initialize the Output:** Create an output grid with the same dimensions as the input grid. Fill the entire output grid with azure (color 8).
4.  **Draw Vertical Line:** Starting from the intersection's y-coordinate, draw a vertical line of blue (color 1) pixels upwards and downwards. The lines stop at the boundaries of the input grid.
5.  **Draw Horizontal Line:** Starting from the intersection's x-coordinate, draw a horizontal line of blue (color 1) pixels to the left and to the right. The lines stop at the boundaries of the input grid.
6. **Replace Intersection:** Change the value of the intersection pixel in the output grid to azure.
7. **Handle no intersection**: if no intersection, return the input grid.
"""

import numpy as np

def find_intersection(input_grid):
    # Find existing horizontal and vertical lines.
    rows, cols = input_grid.shape
    horizontal_line = None
    vertical_line = None

    for r in range(rows):
        unique_colors = np.unique(input_grid[r, :])
        non_background_colors = [c for c in unique_colors if c != 8 and c != 0]
        if len(non_background_colors) > 0:
            horizontal_line = r
            break

    for c in range(cols):
        unique_colors = np.unique(input_grid[:, c])
        non_background_colors = [c for c in unique_colors if c != 8 and c != 0]
        if len(non_background_colors) > 0:
            vertical_line = c
            break

    if horizontal_line is not None and vertical_line is not None:
        return vertical_line, horizontal_line  # x, y
    else:
        return None

def transform(input_grid):
    # Find intersection of existing lines.
    intersection = find_intersection(input_grid)

    # Handle no intersection case.
    if intersection is None:
        return input_grid

    # Initialize output_grid with azure (8).
    output_grid = np.full(np.shape(input_grid), 8)
    input_height, input_width = input_grid.shape
    seed_x, seed_y = intersection

    # Draw Vertical Line.
    for y in range(input_height):
        output_grid[y, seed_x] = 1

    # Draw Horizontal Line
    for x in range(input_width):
        output_grid[seed_y, x] = 1
        
    # Replace Intersection
    output_grid[seed_y, seed_x] = 8

    return output_grid