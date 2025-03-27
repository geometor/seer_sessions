"""
1.  **Identify Objects:** Determine all contiguous objects (blocks of the same color) in the input grid.

2.  **Hypothetical Maroon Movement:** Identify all maroon (9) objects.  For each maroon object, determine the set of positions its pixels *would* occupy if the entire object were moved up by one row.

3.  **Interaction Check:**
    *   Iterate through all *other* objects (non-maroon).
    *   For each object, check if any of its pixels are *directly below* any of the *hypothetical* new positions of the maroon objects.

4.  **Transformations:**
    *   If a grey(5) object is directly below where a maroon object *would* be, change all pixels in that grey object to orange (7).

5.  **Output:** Create the output grid:
    *   The maroon objects are placed in their new positions.
    *   Objects that have changed color based on the interaction rules are updated.
    *   All other pixels in the grid remain unchanged from the input.
    *   If there is an empty space above the original nine, replace it with a zero.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row, col] or grid[row, col] != color:
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                obj = []
                dfs(r, c, grid[r, c], obj)
                if obj:
                    objects.append((grid[r, c], obj))  # Store color and object
    return objects

def hypothetical_move(obj_coords, rows):
    """Calculates the new positions if an object were moved up one row."""
    new_coords = []
    for r, c in obj_coords:
        if r > 0:  # Check if the object can move up
            new_coords.append((r - 1, c))
    return new_coords

def is_directly_below(obj_pixel, hypothetical_maroon_positions):
    """Checks if a pixel is directly below any of the hypothetical maroon positions."""
    r, c = obj_pixel
    return (r + 1, c) in hypothetical_maroon_positions

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Identify objects
    objects = find_objects(input_grid)

    # Locate maroon (9) objects and calculate hypothetical new positions
    maroon_objects = [obj for color, obj in objects if color == 9]
    hypothetical_maroon_positions = []
    for _, obj_coords in maroon_objects:
        hypothetical_maroon_positions.extend(hypothetical_move(obj_coords, rows))

    # Iterate and transform based on interactions
    for color, obj_coords in objects:
        if color == 5:  # Check for grey objects
            for r,c in obj_coords:
                for hr, hc in hypothetical_maroon_positions:
                    if r+1 == hr and c == hc:
                        output_grid[r,c] = 7
                        break #one is enough to change
        elif color == 9: #Handle nines
            for r, c in obj_coords:
                #set to zero if the object is moved, otherwise it's the same
                if r > 0:
                    output_grid[r-1,c] = 9
                if (r-1, c) not in hypothetical_maroon_positions:
                    output_grid[r,c] = input_grid[r,c]
                else:
                    output_grid[r,c] = 0 #was nine, now blank because it moved up

    return output_grid