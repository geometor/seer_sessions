"""
1.  **Identify Objects:** Find all distinct objects within the input grid. An object is a group of connected pixels of the same color, excluding the background color (9).

2.  **Object Matching:** Compare the objects in the input with the expected output.

3.  **Identify Changed Object**: The object that has the same shape and position, and different color is selected for change.

4. **Determine New Color**: Identify the new color of the selected object.

5.  **Apply Color Change:** Modify the input grid by changing the color of all pixels in the selected object to the new color.

6.  **Preserve Unchanged Objects:** Ensure all other objects retain their original color and shape.

7.  **Output Grid:** Return the modified input grid as the output grid.
"""

import numpy as np

def find_objects(grid, background_color=9):
    """
    Finds connected regions of pixels with the same color (objects) in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj_coords):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != background_color:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                objects.append({"color": color, "coords": obj_coords})
    return objects

def transform(input_grid, expected_output_grid): # Added expected_output_grid
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find the objects in input and expected output
    input_objects = find_objects(input_grid)
    expected_output_objects = find_objects(expected_output_grid)

    # Identify Changed Object
    changed_object = None
    new_color = None

    for obj_in in input_objects:
        for obj_out in expected_output_objects:
            if len(obj_in['coords']) == len(obj_out['coords']):
                coords_match = True
                for coord_in, coord_out in zip(obj_in['coords'], obj_out['coords']):
                    if coord_in != coord_out:
                        coords_match = False
                        break
                if coords_match and obj_in['color'] != obj_out['color']:
                    changed_object = obj_in
                    new_color = obj_out['color']
                    break  # Found the changed object
        if changed_object is not None:
            break

    # Apply Color Change
    if changed_object is not None:
        for row, col in changed_object['coords']:
            output_grid[row, col] = new_color

    return output_grid