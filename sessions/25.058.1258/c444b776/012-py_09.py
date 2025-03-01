"""
1.  **Object Identification:** Identify distinct objects in the input grid. An object is a contiguous block of pixels of the same color.
2.  **Iterate through Objects:** For each object in the input grid:
3.  **Look for Reflection:** Check if a mirrored counterpart of the object exists in the output grid. "Mirrored" means the counterpart has the same shape and size but is potentially flipped (reflected) across a vertical or horizontal axis.
4. **Local Axis:** If a mirrored counterpart is found, determine the *local* axis of reflection. The axis could be a line of a specific color within the object, adjacent to the object, or even an imaginary line. The axis does not need to extend across the entire grid.
5. **Partial Reflection:** If only some objects have mirrored counterparts, perform the reflection only for those objects.
6. **Object Disappearance/Appearance:** If the Input has no mirrored objects in Output, the object disappears.
7. **Axis Persistence:** If an axis is part of the identified objects, it should remain unchanged.
"""

import numpy as np

def get_objects(grid):
    """Identifies distinct objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for i in range(rows):
        for j in range(cols):
            if not visited[i, j]:
                obj_pixels = []
                dfs(i, j, grid[i, j], obj_pixels)
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def is_mirrored(obj1, obj2, axis_type, axis_pos):
    """Checks if obj2 is a mirrored counterpart of obj1 across the given axis."""

    if len(obj1) != len(obj2):
        return False

    obj1_coords = np.array(obj1)
    obj2_coords = np.array(obj2)

    if axis_type == 'vertical':
        # Reflect obj1 coordinates across the vertical axis
        reflected_obj1_coords = obj1_coords.copy()
        reflected_obj1_coords[:, 1] = 2 * axis_pos - reflected_obj1_coords[:, 1]

    elif axis_type == 'horizontal':
        # Reflect obj1 coordinates across the horizontal axis
        reflected_obj1_coords = obj1_coords.copy()
        reflected_obj1_coords[:, 0] = 2 * axis_pos - reflected_obj1_coords[:, 0]
    else:
        return False #invalid axis

    # Sort both the reflected coordinates and obj2 coordinates to ensure consistent comparison
    reflected_obj1_coords_sorted = sorted(map(tuple, reflected_obj1_coords))
    obj2_coords_sorted   = sorted(map(tuple,obj2_coords))

    return reflected_obj1_coords_sorted == obj2_coords_sorted


def find_axis(obj1, obj2, grid):
    """Finds the local axis of reflection between two objects."""
    # Find bounding boxes
    min_row1, min_col1 = np.min(obj1, axis=0)
    max_row1, max_col1 = np.max(obj1, axis=0)
    min_row2, min_col2 = np.min(obj2, axis=0)
    max_row2, max_col2 = np.max(obj2, axis=0)

    # Check for vertical axis
    if max_row1 == max_row2 and min_row1 == min_row2:  # Same height
        if (max_col1 + 1 == min_col2 -1) or (max_col1 + 1 == min_col2) or (max_col1 == min_col2-1): #obj1 right obj2 left
             axis_pos = (max_col1 + min_col2) // 2
             return axis_pos, "vertical"
        elif (max_col2 + 1 == min_col1 - 1) or (max_col2 +1 == min_col1) or (max_col2 == min_col1 -1): #obj2 right obj1 left
             axis_pos = (max_col2 + min_col1) // 2
             return axis_pos, "vertical"

    # Check for horizontal axis
    if max_col1 == max_col2 and min_col1 == min_col2: # Same width
        if (max_row1 + 1 == min_row2 - 1) or (max_row1 + 1 == min_row2) or (max_row1 == min_row2 -1): # obj1 top obj2 bottom
            axis_pos = (max_row1 + min_row2) // 2
            return axis_pos, "horizontal"
        elif (max_row2 + 1 == min_row1 - 1) or (max_row2 + 1 == min_row1) or (max_row2 == min_row1-1):#obj2 top obj1 bottom
            axis_pos = (max_row2 + min_row1) // 2
            return axis_pos, "horizontal"

    return -1, None  # No axis found


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    input_objects = get_objects(input_grid)

    # Create a dictionary to store objects
    output_objects_dict = {}

    for obj in input_objects:
        color = input_grid[obj[0]]
        output_objects_dict[tuple(obj)] =  {'processed':False, 'color':color}

    # check for reflection between input objects
    for obj1_key in list(output_objects_dict.keys()):
        obj1_info = output_objects_dict[obj1_key]
        if obj1_info['processed']:
            continue

        obj1 = list(obj1_key)
        obj1_color = obj1_info['color']

        for obj2_key in list(output_objects_dict.keys()):
             if obj1_key == obj2_key: #skip if the object is the same
                continue

             obj2_info = output_objects_dict[obj2_key]
             obj2 = list(obj2_key)
             obj2_color = obj2_info['color']

             if obj1_color != obj2_color:
                 continue

             axis_pos, axis_type = find_axis(obj1, obj2, input_grid)

             if axis_type and is_mirrored(obj1, obj2, axis_type, axis_pos):
                 # Copy both objects to their position in the output
                 for row, col in obj1:
                     output_grid[row, col] = input_grid[row, col]

                 for row, col in obj2:
                    output_grid[row, col] = input_grid[row, col]

                 # Mark as processed
                 output_objects_dict[obj1_key]['processed'] = True
                 output_objects_dict[obj2_key]['processed'] = True
                 break # Go to the next object since this reflection is done

    # Copy non reflected objects
    for obj_key, obj_info in output_objects_dict.items():
        if not obj_info['processed']:
            obj = list(obj_key)
            for row, col in obj:
                output_grid[row, col] = input_grid[row, col]

    return output_grid