# 6150a2bd • 006 • refine_coder

---
```python
"""
The transformation performs a 90-degree clockwise rotation of a single, non-zero colored object within the grid. If the object is not square (dimensions of height and width are not equal), then the rotation is performed on the minimal bounding box of that object, using the center of the bounding box as the point of rotation. If there are multiple colored objects or the bounding box calculation is not possible then a different, unknown transformation applies.
"""

import numpy as np

def get_bounding_box(grid):
    """
    Finds the bounding box of the non-zero elements in a grid.

    Args:
        grid: A 2D list representing the grid.

    Returns:
        A tuple (min_row, max_row, min_col, max_col) representing the bounding box,
        or None if no non-zero elements are found.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    min_row, max_row = rows, -1
    min_col, max_col = cols, -1

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0:
                min_row = min(min_row, i)
                max_row = max(max_row, i)
                min_col = min(min_col, j)
                max_col = max(max_col, j)

    if max_row == -1:  # No non-zero elements found
        return None

    return min_row, max_row, min_col, max_col

def rotate_point_around_center(point, center, k=1):
    """Rotates a point around a center point 90 degrees clockwise (k=1), counterclockwise (k=-1), 180 (k=2)"""
    row, col = point
    center_row, center_col = center
    
    # Translate the point to the origin (relative to the center)
    translated_row = row - center_row
    translated_col = col - center_col
    
    for _ in range(k):
         # Rotate 90 degrees clockwise: (row, col) -> (col, -row)
        rotated_row, rotated_col = translated_col, -translated_row
        translated_row, translated_col = rotated_row, rotated_col
    
    # Translate back to the original coordinate system
    final_row = rotated_row + center_row
    final_col = rotated_col + center_col
    
    return final_row, final_col


def transform(input_grid):
    # Find the bounding box of the non-zero elements
    bbox = get_bounding_box(input_grid)

    if bbox is None:  # Handle empty grid or grid with only zeros
        return input_grid

    min_row, max_row, min_col, max_col = bbox

    # Calculate center of bounding box
    center_row = (min_row + max_row) / 2
    center_col = (min_col + max_col) / 2


    # Initialize output grid with zeros, same size as input
    output_grid = [[0] * len(input_grid[0]) for _ in range(len(input_grid))]

    # Rotate each non-zero pixel within the bounding box
    for i in range(len(input_grid)):
        for j in range(len(input_grid[0])):
            if input_grid[i][j] != 0:
                # Rotate point around the center
                rotated_row, rotated_col = rotate_point_around_center((i, j), (center_row, center_col))

                # Check bounds and set pixel in the output grid
                if 0 <= int(rotated_row) < len(output_grid) and 0 <= int(rotated_col) < len(output_grid[0]):
                     output_grid[int(rotated_row)][int(rotated_col)] = input_grid[i][j]
    return output_grid
```
