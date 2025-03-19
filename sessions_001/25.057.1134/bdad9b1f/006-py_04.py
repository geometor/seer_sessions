"""
1.  **Identify Objects:** Locate all distinct contiguous colored regions (objects) in the input grid.

2.  **Check for Horizontal Lines:** Iterate through each identified object. Determine if an object is a horizontal line. A horizontal line is defined as an object where all pixels have the same row coordinate and the same color.

3.  **Extend Horizontal Lines:** If an object is a horizontal line, extend it to the right, one cell at a time, maintaining the original color.

4.  **Meeting Point and Stop Condition:** Stop the extension when either:
    *   The edge of the grid is reached.
    *   A cell is encountered that is *not* empty (value 0) and does *not* have same color of the horizontal line being extended.

5. **Apply Yellow Marker**: If the extension stops because a non-empty, non-matching color cell (an object) is encountered, change the *last* extended cell to yellow (4) before stopping.

6.  **Preserve Other Objects:** Copy any objects that are not horizontal lines to the output, keeping their original positions and colors.
7. **Fill Remaining Cells**: Any cell not part of the transformation should be 0 (empty/white)
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append(obj)
    return objects

def is_horizontal_line(obj):
    """Checks if an object is a horizontal line."""
    if not obj:
        return False
    first_row = obj[0][0]
    return all(pixel[0] == first_row for pixel in obj)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Copy and extend objects
    for obj in objects:
        first_pixel = obj[0]
        color = input_grid[first_pixel]

        # Check if the object is a horizontal line
        if is_horizontal_line(obj):
            # Copy the horizontal line
            for r, c in obj:
                output_grid[r, c] = input_grid[r, c]

            # Start extending it.
            row = first_pixel[0]
            col = obj[-1][1]  # last pixel to start extending

            while col + 1 < output_grid.shape[1]:
                col += 1
                # Stop if not empty and color doesn't match
                if input_grid[row, col] != 0 and input_grid[row,col] != color:
                    output_grid[row, col - 1] = 4  # meeting point color
                    break
                else:
                    output_grid[row, col] = color
        else:
            # Copy other object type
            for r, c in obj:
                output_grid[r, c] = input_grid[r, c]

    return output_grid