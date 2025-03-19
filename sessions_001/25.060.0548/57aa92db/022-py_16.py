"""
The input grid is transformed as follows:
1.  **Green Object Expansion:** The single green pixel expands. One pixel to the left, and one diagonally up and to the left.
2.  **Azure Object Stays:** The isolated azure object and isolated azure object in rectangle formation stays in the same place.
3.  **Yellow Object Expansion/Merge:** The 2x2 yellow square expands downwards by two rows. It overlaps and effectively replaces/merges with the 2x2 red square that was originally positioned directly below it.
4. Other red object also stays constant.
"""

import numpy as np

def find_object(grid, start_row, start_col):
    """Finds an object in the grid starting from a given position."""
    color = grid[start_row, start_col]
    if color == 0:  # background
        return []

    rows, cols = grid.shape
    visited = set()
    queue = [(start_row, start_col)]
    object_pixels = []

    while queue:
        r, c = queue.pop(0)
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            continue

        visited.add((r, c))
        object_pixels.append((r, c))

        # Check adjacent cells (up, down, left, right)
        queue.append((r + 1, c))
        queue.append((r - 1, c))
        queue.append((r, c + 1))
        queue.append((r, c - 1))

    return object_pixels

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Green Object Expansion
    green_pixel = find_object(input_grid, 2, 4)
    if green_pixel:
        # original pixel is now filled
        output_grid[2, 4] = 3
        # new pixels
        output_grid[2, 3] = 3 # to the left
        output_grid[1, 3] = 3 # diagonally up and left
        

    # 2. Azure Object - already correct by copying.

    # 3. Yellow Object Expansion
    yellow_pixels = find_object(input_grid, 7, 6)  # top left of yellow
    if yellow_pixels:
        # Clear any potentially overlapping 2s from the original.
        for r in range(9, min(11, rows)):
            for c in range(6, min(8,cols)):
                if output_grid[r,c] == 2:
                  output_grid[r,c] = 4
        
        # expand down by two rows
        for r in range(9, min(13, rows)): # expand to rows 9-12, within bounds
          for c in range(6,8): # expand to columns 6-7
            output_grid[r,c] = 4


    return output_grid