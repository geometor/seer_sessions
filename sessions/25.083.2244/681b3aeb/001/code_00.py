"""
1.  **Identify Objects:** Scan the input grid and identify all distinct, contiguous blocks of non-zero (non-white) colored pixels. Each of these blocks is considered an object.
2.  **Object columns** Iterate through the identified objects, taking one object at a time.
3. **Create result array.** Starting with an empty array, append each object's color values to the result array, in a column sorted by object order as they appear in the columns, starting from the upper right corner, then left, then down.
4.  **Arrange in Output Grid:** Construct a new, smaller output grid. First object goes in the last column, other objects are to its left. The row index starts from the bottom of the array, and for each distinct object it goes up. The colors are aligned on the right and bottom.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous blocks of non-zero pixels as objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(obj_pixels)
    return objects


def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Sort objects by column, then row (top-right first)
    objects.sort(key=lambda obj: (-min(col for _, col in obj), min(row for row, _ in obj)), reverse=False)

    # Create result array
    result_array = []
    for obj_pixels in objects:
        # Extract unique colors and sort them? No, maintain original order within the object.
        colors = [input_grid[row, col] for row, col in obj_pixels]
        result_array.append(colors)


    # Determine output grid dimensions
    max_height = max(len(obj) for obj in result_array)
    num_cols = len(result_array)
    output_grid = np.zeros((max_height, num_cols), dtype=int)


    # Populate the output grid
    for j, obj_colors in enumerate(result_array):
        for i, color in enumerate(obj_colors):
            output_grid[max_height - len(obj_colors) + i, num_cols - 1- j] = color


    return output_grid