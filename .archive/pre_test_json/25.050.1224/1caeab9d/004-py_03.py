"""
The transformation involves identifying three 3x2 rectangles (red, blue, and yellow) in the input grid and repositioning them vertically such that they are all aligned in the sixth row (index 5) of the output grid. The relative horizontal positions of the rectangles are maintained.
"""

import numpy as np

def find_objects_3x2(grid):
    """Finds 3x2 rectangle objects in the grid."""
    objects = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 2):
            rectangle = grid[r:r+2, c:c+3]
            if np.all(rectangle == rectangle[0,0]) and rectangle[0,0] != 0:
                objects.append({'color': rectangle[0,0], 'position': (r, c)})
    return objects

def transform(input_grid):
    """
    Transforms the input grid by moving the three 3x2 rectangles to the sixth row.
    """
    # Initialize output grid as a zero array with the same shape as the input
    output_grid = np.zeros_like(input_grid)

    # Find the 3x2 rectangle objects
    objects = find_objects_3x2(input_grid)

    # Move each object to the sixth row (row index 5)
    for obj in objects:
        color = obj['color']
        c = obj['position'][1] # Keep the original column
        output_grid[5:7, c:c+3] = color

    return output_grid