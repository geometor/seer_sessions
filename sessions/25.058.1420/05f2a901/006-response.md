# 05f2a901 • 006 • refine_coder

---
```python
"""
1.  **Identify Objects:** Identify two objects within the grid: a red object (color 2) and an azure object (color 8).
2.  **Azure Object Remains:** The azure object (color 8) remains in its original position and does not change.
3. **Red Object Cleared:** The original position of the red object becomes empty (all pixels set to 0).
4.  **Red Object Shape:** The shape of the red object in the input is determined.
5.  **Copy Red Shape:** A copy of the red object's shape is placed in the output grid based on the location of the azure object:
    *   If the azure object exists outside of the red object's bounding box, the copy is positioned such that, what was the bottom-right corner pixel of the azure object in the input grid, is the top-right pixel of the copied red object.
    *   If the azure object is within the bounding box of the red object, the azure object becomes the geometric center of the copied red shape. If the dimensions of the red shape require a non-integer center, round down to the closest pixel.
6. **Output is otherwise a copy of Input.**
"""

import numpy as np

def find_object(grid, color):
    """Finds the coordinates of an object of the specified color."""
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    if len(coords) == 0:
        return None
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    return min_row, min_col, max_row, max_col

def is_inside_bounding_box(point, bbox):
    """Checks if a point is inside a bounding box."""
    if bbox is None:
        return False
    r, c = point
    min_row, min_col, max_row, max_col = bbox
    return min_row <= r <= max_row and min_col <= c <= max_col

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Find the red and azure objects.
    red_coords = find_object(input_grid, 2)
    azure_coords = find_object(input_grid, 8)

    # Clear initial red object position
    for r, c in red_coords:
        output_grid[r, c] = 0

    #  azure object remains in its original position (already in output_grid)

    # Determine the shift and add object to new position
    if len(red_coords) > 0 and len(azure_coords) > 0:
        red_bbox = get_bounding_box(red_coords)
        azure_bbox = get_bounding_box(azure_coords)
        
        # Find bottom-right of azure object
        azure_br_row, azure_br_col = azure_bbox[2], azure_bbox[3]

        # Get dimensions of Red object
        red_height = red_bbox[2] - red_bbox[0] + 1
        red_width = red_bbox[3] - red_bbox[1] + 1
        
        if all(is_inside_bounding_box((r,c), red_bbox) for r, c in azure_coords): # Azure is within Red
             # Calculate center shift for red object.
            center_row_shift = azure_br_row - (red_height // 2) - red_bbox[0]
            center_col_shift = azure_br_col - (red_width // 2) - red_bbox[1]
            
            for r, c in red_coords:
                new_row = r + center_row_shift
                new_col = c + center_col_shift
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                     output_grid[new_row, new_col] = 2
        
        else: # Azure outside Red
            # Calculate top-right shift for the red object.
            row_shift = azure_br_row - red_bbox[0]
            col_shift = azure_br_col - red_bbox[3]

            for r, c in red_coords:
                new_row = r + row_shift
                new_col = c + col_shift
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                     output_grid[new_row, new_col] = 2


    return output_grid
```
