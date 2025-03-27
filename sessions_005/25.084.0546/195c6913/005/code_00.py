"""
Transforms an input grid based on a set of rules involving object identification,
enclosure detection, and conditional color changes, focusing on a more
precise and iterative approach to rule implementation.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects within the grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of objects, where each object is a set of (row, col) tuples.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object, color):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.add((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, current_object, color)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                current_object = set()
                dfs(row, col, current_object, grid[row, col])
                objects.append(current_object)
    return objects

def is_enclosed(object_coords, grid):
    """
    Checks if an object is fully enclosed by another single color.

    Returns:
      The enclosing color if enclosed, otherwise None.
    """
    rows, cols = grid.shape
    neighbor_colors = set()
    
    for row, col in object_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
               return None # touching edge
            if (nr, nc) not in object_coords:
              neighbor_colors.add(grid[nr,nc])

    if len(neighbor_colors) == 1:
       return neighbor_colors.pop()
    else:
       return None

def get_bounding_box(coords):
    """
    Returns the bounding box of a set of coordinates as (min_row, min_col, max_row, max_col).
    """
    if not coords:
        return None
    min_row = min(r for r, _ in coords)
    min_col = min(c for _, c in coords)
    max_row = max(r for r, _ in coords)
    max_col = max(c for _, c in coords)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """
    Applies the transformation to the input grid.
    """
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape
    objects = find_objects(input_grid)

    # Apply background color change (observed in example 3) - ALL 0 become 1
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 0:
                output_grid[r,c] = 1

    # Apply contextual color changes based on enclosure
    for obj in objects:
        enclosing_color = is_enclosed(obj, input_grid)
        if enclosing_color is not None:
            first_coord = list(obj)[0]
            obj_color = input_grid[first_coord]

            # Example 1: "Color 2 regions within color 3 regions become color 8 or color 0 based on relative location"
            if obj_color == 2 and enclosing_color == 3:
                min_row, min_col, max_row, max_col = get_bounding_box(obj)
                center_row = (min_row + max_row) // 2
                # center_col = (min_col + max_col) // 2 # Not used

                for row, col in obj:
                    if row < center_row:
                        output_grid[row, col] = 8
                    else:
                        output_grid[row, col] = 0

            # Example 2: Color 4 and 1 inside 8.  Flipping and color changes.
            elif obj_color in (1, 4) and enclosing_color == 8:
                # Get bounding box
                min_row, min_col, max_row, max_col = get_bounding_box(obj)
                
                # Find center of bounding box
                center_row = (min_row + max_row) // 2
                center_col = (min_col + max_col) // 2

                # Create a copy of the object coordinates to avoid modifying during iteration
                coords = list(obj)
                
                for r, c in coords:
                    # Reflect across the horizontal center
                    new_row = (max_row - (r - min_row))

                    # Reflect across vertical center
                    new_col = (max_col - (c - min_col))
                    
                    #Check if reflected location is in original object
                    if (new_row, new_col) not in obj:
                        continue

                    # Apply color changes based on original color
                    if input_grid[r, c] == 1:
                        output_grid[new_row, new_col] = 4
                    elif input_grid[r, c] == 4:
                        output_grid[new_row, new_col] = 1

            # Example 3: "Color 4 surrounded by 1, 2, or 3 remains 4"
            elif obj_color == 4 and enclosing_color in [1, 2, 3]:
                for row, col in obj:
                    output_grid[row, col] = 4  # Keep as 4

    return output_grid