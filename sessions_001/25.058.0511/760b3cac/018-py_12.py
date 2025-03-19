"""
The transformation involves identifying an azure (8) shape and a yellow (4) shape. The yellow shape is preserved. The original azure shape is removed. A new azure shape is created based on these rules: 1) If there's a yellow shape, and the row below it is empty, the new azure shape is placed there, with the width of the original azure shape. 2) If there's a yellow shape, and the row above it is empty, the new azure shape is placed there, with the width of the yellow shape.
"""

import numpy as np

def find_shape(grid, color):
    """Finds the coordinates of a shape of a specific color."""
    coords = np.argwhere(grid == color)
    return coords if coords.size > 0 else None

def get_shape_dimensions(coords):
    """Calculates the bounding box dimensions of a shape."""
    if coords is None:
        return None
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    width = max_col - min_col + 1
    height = max_row - min_row + 1
    return {'min_row': min_row, 'max_row': max_row, 'min_col': min_col, 'max_col': max_col, 'width': width, 'height': height}

def is_row_empty(grid, row):
    """Checks if a given row is empty (all 0s)."""
    return np.all(grid[row] == 0)

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)

    # Identify objects.
    azure_coords = find_shape(input_grid, 8)
    yellow_coords = find_shape(input_grid, 4)

    # Preserve yellow shape.
    if yellow_coords is not None:
        for r, c in yellow_coords:
            output_grid[r, c] = 4

    # Remove original azure shape.
    if azure_coords is not None:
        for r, c in azure_coords:
            output_grid[r, c] = 0

    # Conditional azure placement.
    if yellow_coords is not None:
        yellow_dims = get_shape_dimensions(yellow_coords)
        azure_dims = get_shape_dimensions(azure_coords)

        row_below = yellow_dims['max_row'] + 1
        row_above = yellow_dims['min_row'] - 1
        
        if row_below < output_grid.shape[0] and is_row_empty(output_grid, row_below):
            # Place below, matching original azure width.
            for c in range(azure_dims['min_col'], azure_dims['max_col'] + 1):
                if 0 <= c < output_grid.shape[1]: # added bounds check
                    output_grid[row_below, c] = 8
        elif row_above >= 0 and is_row_empty(output_grid, row_above):
            # Place above, matching yellow width.
            for c in range(yellow_dims['min_col'], yellow_dims['max_col'] + 1):
                output_grid[row_above, c] = 8

    return output_grid