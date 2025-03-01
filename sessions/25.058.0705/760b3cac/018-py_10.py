"""
1.  **Identify Objects:** Find all contiguous blocks (objects) of azure (8) and yellow (4) pixels.
2.  **Preserve Yellow:** Keep all yellow (4) objects in their original positions in the output grid.
3.  **Shift and Duplicate Azure:** For each azure (8) object:
    *   **Shift:** Shift the entire object one column to the left.
    *   **Duplicate:** Create an exact copy of the *original* azure object, placing it directly adjacent to the *shifted* object, such that the leftmost edge of the duplicate aligns with the original leftmost edge of the unshifted object. The copied object fills the space vacated by the original.
4. **Maintain Vertical Order** The azure objects are always vertically above the yellow.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    Returns a dictionary of objects, where keys are colors and values are lists of positions.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, positions):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        positions.append((row, col))
        dfs(row + 1, col, color, positions)
        dfs(row - 1, col, color, positions)
        dfs(row, col + 1, color, positions)
        dfs(row, col - 1, col, color, positions)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                if color != 0:
                    positions = []
                    dfs(row, col, color, positions)
                    if color not in objects:
                        objects[color] = []
                    objects[color].append(positions)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects
    objects = find_objects(input_grid)

    # change output pixels - Preserve Yellow
    if 4 in objects:
        for yellow_object in objects[4]:
          for row, col in yellow_object:
              output_grid[row, col] = 4

    # Transform Azure: shift and duplicate
    if 8 in objects:
        for azure_object in objects[8]:
            # Find the original leftmost column
            original_leftmost_col = min(pos[1] for pos in azure_object)

            # Shift each pixel of the object one column to the left
            for row, col in azure_object:
                new_col = col - 1
                if new_col >= 0:
                    output_grid[row, new_col] = 8

            # Duplicate the original object, placing it based on the original leftmost column
            for row, col in azure_object:
                original_col = col
                if original_col < cols:  # Ensure we stay within bounds
                    output_grid[row, original_col] = 8

    return output_grid