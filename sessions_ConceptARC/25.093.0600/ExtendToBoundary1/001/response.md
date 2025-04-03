```python
"""
Identifies a single contiguous non-zero shape in the input grid.
Calculates the shape's bounding box, height, width, and center coordinates.
Compares the height and width:
- If height > width, draws a vertical line downwards from the center column, starting below the shape, to the bottom edge of the grid, using the shape's color.
- If width >= height, draws a horizontal line rightwards from the center row, starting to the right of the shape, to the right edge of the grid, using the shape's color.
The output grid is the input grid with this added line.
"""

import numpy as np

def find_shape_properties(grid):
    """
    Finds the single non-zero shape and returns its properties.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: color, min_r, max_r, min_c, max_c, height, width, center_r, center_c
               Returns None if no non-zero shape is found.
    """
    # Find indices of non-zero elements
    non_zero_indices = np.argwhere(grid > 0)

    if non_zero_indices.shape[0] == 0:
        return None # No shape found

    # Assume a single shape with a single color
    color = grid[non_zero_indices[0, 0], non_zero_indices[0, 1]]

    # Determine bounding box
    min_r = np.min(non_zero_indices[:, 0])
    max_r = np.max(non_zero_indices[:, 0])
    min_c = np.min(non_zero_indices[:, 1])
    max_c = np.max(non_zero_indices[:, 1])

    # Calculate height and width
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Calculate center coordinates (integer division)
    center_r = (min_r + max_r) // 2
    center_c = (min_c + max_c) // 2

    return color, min_r, max_r, min_c, max_c, height, width, center_r, center_c


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    grid_height, grid_width = grid.shape

    # Find the properties of the non-zero shape
    shape_props = find_shape_properties(grid)

    # If no shape is found, return the original grid
    if shape_props is None:
        return output_grid.tolist()

    color, min_r, max_r, min_c, max_c, height, width, center_r, center_c = shape_props

    # Compare height and width to determine line orientation
    if height > width:
        # Draw vertical line downwards from below the shape's bottom edge in the center column
        start_row = max_r + 1
        for r in range(start_row, grid_height):
            # Check bounds just in case center_c is somehow out of bounds (shouldn't happen with valid inputs)
            if 0 <= r < grid_height and 0 <= center_c < grid_width:
                 output_grid[r, center_c] = color
    elif width >= height:
        # Draw horizontal line rightwards from the right of the shape's edge in the center row
        start_col = max_c + 1
        for c in range(start_col, grid_width):
             # Check bounds just in case center_r is somehow out of bounds
             if 0 <= center_r < grid_height and 0 <= c < grid_width:
                output_grid[center_r, c] = color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```