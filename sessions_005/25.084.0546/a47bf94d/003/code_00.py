"""
1. Identify Objects: Locate all contiguous rectangular blocks of the same color in the input grid.

2. Color-Specific Transformations:
    *   All objects that do not have color azure (8) are changed to white.
    *   Each object of color azure (8) is duplicated using color of the object and reflected
        horizontally.
    *   Insert single pixels of the color of the reflected object, respecting
        horizontal symmetry across the middle columns. For each row, and for each non-azure object, insert one
        pixel for each side of the azure object.

3. Create output: Using the transformed objects and background, reconstruct the output grid with the same dimensions as the input grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                objects.append((color, obj))
    return objects

def reflect_object(obj, width):
    """Reflects an object horizontally across the center of the grid."""
    reflected_obj = []
    for r, c in obj:
        reflected_c = width - 1 - c
        reflected_obj.append((r, reflected_c))
    return reflected_obj

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Process each object based on color
    for color, obj_coords in objects:
        if color == 8: # azure
            # keep original object
            for r, c in obj_coords:
                    output_grid[r,c] = color

            # Reflect azure objects
            reflected_coords = reflect_object(obj_coords, cols)
            for r, c in reflected_coords:
                output_grid[r, c] = color
        

    for color, obj_coords in objects:
        # get distinct rows
        obj_rows = sorted(list(set([r for r,c in obj_coords])))

        if color != 8 and color != 0:  # Process non-azure, non-white objects

            for row in obj_rows:
                # insert new object
                insert_color = color

                # find azure objects to the left
                left_azure_count = 0
                for c_iter in range(0, cols//2):
                    if input_grid[row, c_iter] == 8:
                         left_azure_count += 1
                
                # find azure objects to the right
                right_azure_count = 0
                for c_iter in range(cols//2, cols):
                    if input_grid[row, c_iter] == 8:
                        right_azure_count +=1

                insert_col = cols//2 - 1 - left_azure_count # insert to left
                if insert_col >= 0:
                     output_grid[row, insert_col] = insert_color
                
                insert_col = cols//2 + right_azure_count # insert to right
                if cols%2 == 1: # odd
                    insert_col = cols//2 + right_azure_count # insert to right
                else:
                    insert_col = cols//2-1 + right_azure_count #

                if insert_col < cols:
                    output_grid[row, insert_col] = insert_color
                
    return output_grid