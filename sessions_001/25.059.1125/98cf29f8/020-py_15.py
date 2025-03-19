"""
1.  Identify Objects: Identify all horizontal rows of pixels with the same color. Each row is a separate object.  All objects within a grid have the same width, and objects are separated vertically by one blank row.
2.  Stack Objects: Stack the identified objects vertically in the output grid.
3.  Preserve Order: Maintain the original vertical order of the objects from the input grid.
4.  No Gaps: The objects in the output grid should be adjacent, with no intervening blank rows.
"""

import numpy as np

def find_objects(grid):
    """Identifies distinct objects (horizontal rows of same color)."""
    objects = []
    visited = set()

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited and grid[row, col] != 0:
                color = grid[row, col]
                # Find the end of the horizontal row
                end_col = col
                while end_col < grid.shape[1] and grid[row, end_col] == color:
                    end_col += 1

                # Extract the object (row)
                obj_pixels = [(row, c) for c in range(col, end_col)]
                objects.append((color, obj_pixels))

                # Mark pixels as visited
                for r, c in obj_pixels:
                    visited.add((r, c))
    return objects

def transform(input_grid):
    # Initialize output grid with zeros (all white)
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Sort objects by their row index (preserve original order)
    objects.sort(key=lambda x: x[1][0][0])  # Sort by row of the first pixel

    # Stack objects vertically in the output grid
    current_row = 0
    for color, pixels in objects:
        for r, c in pixels:
            output_grid[current_row, c] = color
        current_row += 1

    return output_grid