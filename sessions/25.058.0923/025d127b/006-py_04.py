"""
1.  Identify Objects: Divide the input grid into distinct objects. An object is a contiguous group of pixels of the same color (excluding white/0), connected horizontally or vertically (not diagonally).

2.  Find Leftmost Column with Object Color: For each object, identify the leftmost column that contains *any* pixels of that object's color.

3. **Conditional Modification:**
   - If an object has pixels in its leftmost identified column, change *only the object-colored* pixels in that column in the output.
   - If there is more than one object, and one object has pixels in a column *before* the other, then change the object-colored pixels in that first column to white.
   - Leave all other pixels (including other objects and pixels of different colors in the same column) unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid based on color contiguity.
    Returns a dictionary where keys are object IDs and values are lists of (row, col) coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, object_id):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        objects.setdefault(object_id, []).append((row, col))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(row + dr, col + dc, color, object_id)

    object_id_counter = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                object_id_counter += 1
                dfs(r, c, grid[r, c], object_id_counter)
    return objects

def get_leftmost_column_with_color(object_coords):
    """
    Returns the column index of the leftmost pixel *of the object's color* in the object.
    """
    return min(col for _, col in object_coords)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find objects
    objects = find_objects(input_grid)

    # Create a list to store (leftmost_column, object_id, object_color) tuples
    object_info = []
    for obj_id, coords in objects.items():
        object_color = input_grid[coords[0][0], coords[0][1]]
        leftmost_col = get_leftmost_column_with_color(coords)
        object_info.append((leftmost_col, obj_id, object_color))

    # Sort objects by their leftmost column
    object_info.sort()

    # Iterate through each object, considering leftmost column
    for leftmost_col, obj_id, object_color in object_info:
        coords = objects[obj_id]

        # Iterate through the pixels in the leftmost column of the *grid*
        for r in range(rows):
            # Check if the current pixel belongs to the current object and is in its leftmost column
            if (r, leftmost_col) in coords and input_grid[r, leftmost_col] == object_color:
                output_grid[r, leftmost_col] = 0  # Change to white


    return output_grid