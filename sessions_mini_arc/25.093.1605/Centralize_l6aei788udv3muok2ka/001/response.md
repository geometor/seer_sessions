```python
"""
Transforms an input grid by identifying a shape (a connected group of identical 
non-zero numbers), calculating the center of its bounding box, and translating 
the shape so its bounding box center aligns with the center of the grid. 
The background is assumed to be 0.
"""

import numpy as np

def _find_shape_and_color(grid):
    """
    Finds the coordinates of all non-zero cells and determines their common value (color).
    Assumes there's only one non-zero value present.
    """
    shape_cells = []
    shape_color = 0
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                shape_cells.append((r, c))
                if shape_color == 0:
                    shape_color = value
                elif value != shape_color:
                    # This case shouldn't happen based on examples, but good to handle
                    raise ValueError("Input grid contains multiple non-zero values.")
    return shape_cells, shape_color

def _get_bounding_box(shape_cells):
    """Calculates the min/max row/col for the shape."""
    if not shape_cells:
        return None # Or raise error, depending on desired behavior for empty shapes
    
    rows = [r for r, c in shape_cells]
    cols = [c for r, c in shape_cells]
    
    min_row = min(rows)
    max_row = max(rows)
    min_col = min(cols)
    max_col = max(cols)
    
    return min_row, max_row, min_col, max_col

def _calculate_center(min_val, max_val):
    """Calculates the center index using floor division."""
    # Using floor division to match the described logic
    return (min_val + max_val) // 2

def transform(input_grid):
    """
    Applies the shape centering transformation.
    
    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert to numpy array for easier handling
    input_array = np.array(input_grid)
    height, width = input_array.shape
    
    # Initialize output grid with zeros
    output_array = np.zeros_like(input_array)

    # 1. Identify Shape and its color
    shape_cells, shape_color = _find_shape_and_color(input_array)
    
    # If no shape found, return the empty grid
    if not shape_cells:
        return output_array.tolist()

    # 2. Find Bounding Box
    min_row, max_row, min_col, max_col = _get_bounding_box(shape_cells)

    # 3. Calculate Input Center (center of the bounding box)
    center_row_input = _calculate_center(min_row, max_row)
    center_col_input = _calculate_center(min_col, max_col)

    # 4. Determine Grid Center
    center_row_grid = (height - 1) // 2 # Use floor division for center index
    center_col_grid = (width - 1) // 2  # Use floor division for center index

    # 5. Calculate Shift required
    delta_row = center_row_grid - center_row_input
    delta_col = center_col_grid - center_col_input

    # 6. Translate Shape
    for r, c in shape_cells:
        new_r = r + delta_row
        new_c = c + delta_col
        
        # Ensure the new coordinates are within the grid bounds
        if 0 <= new_r < height and 0 <= new_c < width:
            output_array[new_r, new_c] = shape_color
            
    # Convert back to list of lists before returning
    return output_array.tolist()

```