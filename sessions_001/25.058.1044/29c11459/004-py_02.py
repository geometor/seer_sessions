"""
1.  **Identify Objects:** Locate the distinct non-zero digits (1 and 2, representing blue and red respectively) in the first row of the input grid.

2.  **Horizontal Expansion:**
    *   Expand the blue object (value 1) to the right, filling cells with 1s.
    *   Expand the red object (value 2) to the left, filling cells with 2s.
    *   Expansion of each object terminates in the middle, such that the objects take up an equal amount of horizontal space.

3.  **Insert Separator:** Place a single cell with the value 5 (grey) between the expanded blue and red regions. This will likely be in the horizontal center of the row between the two objects.

4.  **Other rows**: keep other rows unchanged, filled entirely with 0.
"""

import numpy as np

def find_objects(grid):
    """Finds non-zero objects in the first row of the grid."""
    objects = []
    for x, value in enumerate(grid[0]):
        if value != 0:
            objects.append({'value': value, 'x': x})
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects in the first row
    objects = find_objects(input_grid)
    
    #if there are two distinct objects
    if (len(objects) == 2):

        # Get the x-coordinates of the objects
        x1 = objects[0]['x']
        x2 = objects[1]['x']
        val1 = objects[0]['value']
        val2 = objects[1]['value']

        # Calculate the midpoint
        midpoint = cols // 2

        # Expand the first object to the right until the midpoint
        for x in range(x1, midpoint):
            output_grid[0][x] = val1

        # Expand the second object to the left until the midpoint
        for x in range(midpoint + 1, x2 + 1):
            output_grid[0][x] = val2

        # Insert the separator (5) at the midpoint
        output_grid[0][midpoint] = 5

    return output_grid