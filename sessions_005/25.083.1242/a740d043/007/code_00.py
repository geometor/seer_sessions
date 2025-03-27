"""
1.  **Identify Objects:** Locate all contiguous regions (objects) of non-blue pixels in the input grid. Pixels are considered part of the same object if they are adjacent horizontally or vertically.
2.  **Remove Separators:**  Conceptually remove the blue pixels (value 1), which act as separators between objects.
3.  **Bounding Boxes:** Determine the bounding box for each identified object. The bounding box is the smallest rectangle (defined by `min_row`, `min_col`, `max_row`, `max_col`) that completely encloses the object.
4.  **Vertical Stacking with Horizontal Preservation:** Stack the objects vertically. The height of the output grid is the sum of the heights of all object bounding boxes. The width of the output grid is determined by the range of columns occupied by the stacked objects. Crucially, maintain the relative horizontal positioning of each object according to the starting column (`min_col`) of its bounding box. Place each object's pixels in the output grid by offsetting from the object top by current row and object min column, preserving its column from input.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of non-blue pixels in the grid.
    Returns a list of objects, where each object is a list of (row, col, value) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 1:
            return
        visited.add((r, c))
        current_object.append((r, c, grid[r, c]))
        # Check adjacent cells (up, down, left, right)
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 1 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)

    return objects

def get_bounding_box(obj):
    """
    Calculates the bounding box of an object.
    Returns (min_row, min_col, max_row, max_col).
    """
    min_row = min(r for r, c, _ in obj)
    min_col = min(c for r, c, _ in obj)
    max_row = max(r for r, c, _ in obj)
    max_col = max(c for r, c, _ in obj)
    return (min_row, min_col, max_row, max_col)


def transform(input_grid):
    """
    Transforms the input grid by extracting non-blue shapes and stacking them vertically,
    preserving their relative horizontal positions.
    """
    input_grid = np.array(input_grid)

    # Find non-blue objects
    objects = find_objects(input_grid)

    # Calculate output grid dimensions
    total_height = 0
    min_col_global = float('inf')
    max_col_global = float('-inf')

    for obj in objects:
        min_row, min_col, max_row, max_col = get_bounding_box(obj)
        total_height += (max_row - min_row + 1)
        min_col_global = min(min_col_global, min_col)
        max_col_global = max(max_col_global, max_col)

    output_width = max_col_global - min_col_global + 1

    # Initialize output grid
    output_grid = np.zeros((total_height, output_width), dtype=int)

    # Populate the output grid, preserving relative horizontal positions
    current_row = 0
    for obj in objects:
        min_row, min_col, max_row, max_col = get_bounding_box(obj)

        for r, c, val in obj:
            # Offset column by the global minimum column
            output_grid[r - min_row + current_row, c - min_col_global] = val

        current_row += (max_row - min_row + 1)

    return output_grid.tolist()