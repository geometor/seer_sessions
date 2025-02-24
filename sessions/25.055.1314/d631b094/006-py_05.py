"""
1. Identify Objects: Examine the input grid and identify all distinct objects. An object is defined as a group of orthogonally connected pixels of the same color.
2. Extract Objects: For each identified object, copy its pixel data, preserving its original shape.
3. Create Output Row: create an output array with height of 1.
4. Arrange Objects: Place the extracted objects into the output grid as a single row. Maintain each object's shape, and place the object on the row. The order should be left to right, and top-to-bottom, according to object appearance in the input grid.
"""

import numpy as np
from skimage.measure import label

def get_objects(grid):
    """Identifies and extracts objects from the grid."""
    labeled_grid = label(grid, connectivity=1)
    num_objects = np.max(labeled_grid)
    objects = []
    for i in range(1, num_objects + 1):
        object_mask = (labeled_grid == i)
        object_pixels = np.where(object_mask)
        min_row, min_col = np.min(object_pixels[0]), np.min(object_pixels[1])
        object_shape = (
            object_pixels[0].max() - min_row + 1,
            object_pixels[1].max() - min_col + 1,
        )
        object_data = grid[object_mask].reshape(object_shape)
        
        # Calculate the starting position (top-left corner) of the object in the original grid
        start_position = (min_row, min_col)
        objects.append((object_data, start_position))
    return objects

def transform(input_grid):
    # Identify and extract objects
    objects = get_objects(input_grid)

    # Sort objects based on their top-left corner's row-major order
    objects.sort(key=lambda x: (x[1][0], x[1][1]))  # Sort by row, then column

    # Calculate the total width of the output grid
    total_width = 0
    for obj, _ in objects:
        total_width += obj.shape[1]

    # Create the output grid
    output_grid = np.zeros((1, total_width), dtype=int)

    # Arrange objects in the output grid
    current_col = 0
    for obj, _ in objects:
        height, width = obj.shape
        output_grid[0, current_col:current_col + width] = obj
        current_col += width

    return output_grid