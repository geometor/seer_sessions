"""
1. **Identify Azure Shapes:** Find all connected regions of azure (8) pixels within the input grid.
2. **Bounding Boxes:** For each identified azure shape, determine the minimum bounding box that completely encloses it.
3. **Extract Corners:** From each bounding box, extract the color value of the top-left pixel and the bottom-right pixel.
4. **Construct Output:** Create a 2x2 output grid. Place the color of the top-left pixel of the *first* identified shape's bounding box in the top-left cell of the output grid. Place the color value of the bottom-right pixel of the *last* identified shape's bounding box in the bottom-right cell of the output grid. Fill the remaining two cells of the output grid with white (0). If only one shape detected, the top-left pixel goes to output top-left, and bottom right of the same shape goes to the output bottom-right.
"""

import numpy as np
from scipy.ndimage import label

def find_objects(grid, color):
    """Finds connected regions of a specific color in the grid."""
    colored_grid = (grid == color).astype(int)
    labeled_grid, num_objects = label(colored_grid)
    return labeled_grid, num_objects

def get_bounding_box(labeled_grid, object_label):
    """Calculates the bounding box for a given object label."""
    coords = np.where(labeled_grid == object_label)
    min_row, min_col = np.min(coords, axis=1)
    max_row, max_col = np.max(coords, axis=1)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Find azure objects
    labeled_grid, num_objects = find_objects(input_grid, 8)

    # Initialize output grid
    output_grid = np.zeros((2, 2), dtype=int)

    if num_objects > 0:
        # Get bounding box of the first object
        (first_min_row, first_min_col), _ = get_bounding_box(labeled_grid, 1)
        output_grid[0, 0] = input_grid[first_min_row, first_min_col]

        # Get bounding box of the last object
        _, (last_max_row, last_max_col) = get_bounding_box(labeled_grid, num_objects)
        output_grid[1, 1] = input_grid[last_max_row, last_max_col]

    return output_grid