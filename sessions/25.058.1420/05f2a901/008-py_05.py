"""
1.  **Identify Objects:** Identify two objects: a red object (color 2) and an azure object (color 8).

2.  **Preserve Azure:** The azure object remains in its original position in the output grid.

3. **Clear Original Red:** Remove the red object from its initial position in the output grid (set pixels to 0).

4.  **Copy Red Object:** Create a copy of the red object's shape.

5.  **Reposition Red Object:**
    *   **If the azure object's bounding box is *completely* within the red object's bounding box:** Position the copy of the red object so that the azure object is at its center.  If the center falls between pixels, round the row and column down to the nearest whole pixel.
    *   **Otherwise (if the azure object is not completely inside the red object's bounding box, which includes if they intersect or are disjoint):** Position the copy of the red object such that the bottom-right corner of the azure object's bounding box aligns with the *bottom-right corner* of where the red object was.

6. **Output is otherwise a copy of input.**
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

def is_completely_inside(inner_bbox, outer_bbox):
    """Checks if inner_bbox is completely inside outer_bbox."""
    if inner_bbox is None or outer_bbox is None:
        return False
    in_min_row, in_min_col, in_max_row, in_max_col = inner_bbox
    out_min_row, out_min_col, out_max_row, out_max_col = outer_bbox
    return (out_min_row <= in_min_row and in_max_row <= out_max_row and
            out_min_col <= in_min_col and in_max_col <= out_max_col)

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Find the red and azure objects.
    red_coords = find_object(input_grid, 2)
    azure_coords = find_object(input_grid, 8)

    # Clear initial red object position
    for r, c in red_coords:
        output_grid[r, c] = 0

    #  Azure object remains in its original position (already in output_grid)

    # Determine the shift and add object to new position
    if len(red_coords) > 0 and len(azure_coords) > 0:
        red_bbox = get_bounding_box(red_coords)
        azure_bbox = get_bounding_box(azure_coords)
        
        # Find bottom-right of original red object
        red_br_row, red_br_col = red_bbox[2], red_bbox[3]
        # Find bottom-right of azure
        azure_br_row, azure_br_col = azure_bbox[2], azure_bbox[3]

        # Get dimensions of Red object
        red_height = red_bbox[2] - red_bbox[0] + 1
        red_width = red_bbox[3] - red_bbox[1] + 1
        
        if is_completely_inside(azure_bbox, red_bbox): # Azure is completely within Red
             # Calculate center shift for red object.
            center_row_shift = azure_br_row - (red_height // 2) - red_bbox[0]
            center_col_shift = azure_br_col - (red_width // 2) - red_bbox[1]
            
            for r, c in red_coords:
                new_row = r + center_row_shift
                new_col = c + center_col_shift
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                     output_grid[new_row, new_col] = 2
        
        else: # Azure outside or intersects Red
            # Calculate bottom-right shift for the red object.
            row_shift = azure_br_row - red_br_row
            col_shift = azure_br_col - red_br_col

            for r, c in red_coords:
                new_row = r + row_shift
                new_col = c + col_shift
                if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
                     output_grid[new_row, new_col] = 2

    return output_grid