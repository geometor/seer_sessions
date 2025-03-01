"""
1.  **Identify Objects:** Locate all distinct clusters of contiguous, non-white pixels in the input grid. Each cluster is an object.
2.  **Preserve:** Maintain the structure, count and color of all objects
3. **Reconstruct:** Create an output grid with the same dimensions and background as the input, placing all identified and processed objects in their original positions.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects (contiguous non-zero pixels) in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] == 0:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by identiy, i.e. making a copy
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Create an output grid that's a copy of the input grid
    output_grid = np.copy(input_grid)

    return output_grid.tolist()