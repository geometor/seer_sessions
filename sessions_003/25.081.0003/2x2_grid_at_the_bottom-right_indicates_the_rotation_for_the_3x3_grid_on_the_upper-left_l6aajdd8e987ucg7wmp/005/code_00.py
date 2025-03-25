"""
1.  **Identify Green Components:** Locate all disconnected green (color 3)
    components in the input grid. Each separate contiguous block of green
    pixels is a distinct component.

2.  **Reposition Green Components:** Move each identified green component to
    the top-left region of the output grid.
    *   Maintain the original shape of each green component.
    *   Preserve the relative vertical and horizontal positions *between* the
        green components. Start placing at (0,0), and subsequent components
        are positioned relative to the already placed ones, matching the
        relative positioning they had in the input.
    *   After moving the green components, fill the positions that used to
        have a green object with black pixels (value 0).

3.  **Identify and Remove Blue and Yellow Objects:**
    *   Locate a 2x1 block of blue (color 1) pixels.
    *   Locate a single yellow (color 4) pixel directly adjacent to the 2x1
        blue block.
    *   Remove both the identified blue and yellow objects by setting the
        pixel to 0.

4. **Output Grid:** The output grid should contain the repositioned green
   components and zeros in all other cells.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_object_shape(object_coords):
    min_row = min(r for r, c in object_coords)
    max_row = max(r for r, c in object_coords)
    min_col = min(c for r, c in object_coords)
    max_col = max(c for r, c in object_coords)
    shape = []
    for r, c in object_coords:
        shape.append((r - min_row, c - min_col))
    return shape, (max_row - min_row + 1, max_col - min_col + 1)

def find_2x1_blue_and_adjacent_yellow(grid):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            # Check for 2x1 blue
            if c + 1 < cols and grid[r, c] == 1 and grid[r, c + 1] == 1:
                # Check for adjacent yellow
                if c + 2 < cols and grid[r,c+2] == 4:
                    return (r, c), (r, c + 1), (r, c+2)
                if c - 1 >= 0 and grid[r,c-1] == 4:
                    return (r, c), (r, c + 1), (r, c-1)
                if r + 1 < rows:
                    if grid[r+1,c] == 4:
                        return (r, c), (r, c+1), (r+1, c)
                    if c + 1 < cols and grid[r+1, c+1] == 4:
                        return (r, c), (r, c + 1), (r+1, c+1)
                if r - 1 >= 0:
                    if grid[r-1,c] == 4:
                        return (r, c), (r, c+1), (r-1, c)
                    if c+1 < cols and grid[r-1,c+1] == 4:
                        return (r, c), (r, c + 1), (r-1, c+1)
            elif r + 1 < rows and grid[r,c] == 1 and grid[r+1,c] == 1:
                if c + 1 < cols and grid[r,c+1] == 4:
                    return (r, c), (r+1, c), (r, c+1)
                if r + 1 < rows and c + 1 < cols and grid[r+1, c+1] == 4:
                        return (r, c), (r+1, c), (r+1, c+1)
                if c - 1 >= 0 and grid[r,c-1] == 4:
                    return (r, c), (r+1, c), (r, c-1)
                if r + 1 < rows and c - 1 >= 0 and grid[r+1, c - 1] == 4:
                        return (r, c), (r+1, c), (r+1, c - 1)
                if r + 2 < rows and grid[r+2,c] == 4:
                    return (r,c), (r+1,c), (r+2,c)
                if r - 1 >= 0 and grid[r-1,c] == 4:
                    return (r,c), (r+1,c), (r-1,c)

    return None, None, None


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    input_grid_copy = np.copy(input_grid)

    # Find green components
    green_objects = find_objects(input_grid_copy, 3)

    # Reposition Green Components
    current_row = 0
    current_col = 0
    for obj in green_objects:
        shape, (height, width) = get_object_shape(obj)

        for r, c in shape:
            output_grid[current_row + r, current_col + c] = 3
        current_row += height #simple stack

        #clear object after placement
        for r,c in obj:
            input_grid_copy[r][c] = 0

    # Find and Remove Blue and Yellow Objects
    blue1, blue2, yellow = find_2x1_blue_and_adjacent_yellow(input_grid_copy)
    if blue1:
        input_grid_copy[blue1] = 0
        input_grid_copy[blue2] = 0
        input_grid_copy[yellow] = 0

    return output_grid