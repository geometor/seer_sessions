"""
1.  **Color 9 Removal:**
    *   Iterate through each cell in the grid.
    *   If a cell has color 9, check if *any* of its immediate neighbors (up, down, left, or right) has color 0.
    *   If a cell with color 9 has 0 as a neighbor, change the cell's color to 0.

2.  **Enclosed Object Color Transformation:**
    *   Identify all contiguous objects (blocks of the same non-zero color).
    *   For each object:
        *   Find all colors adjacent to the object (excluding the object's own color and 0).
        *   If there is *only one* such adjacent color, change all pixels in the object to that color.

3.  **Vertical Line Modification:**
    * Scan each column from left to right.
    * For each column:
        * Find the top-most non-zero pixel.
        * If there is *any* other non-zero pixel *below* it in the same column, change the top-most pixel's color to 0.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the coordinates of the four neighbors (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def get_adjacent_colors(grid, r, c):
    """Gets the colors of the four neighbors (up, down, left, right)."""
    rows, cols = grid.shape
    adjacent_colors = set()
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            adjacent_colors.add(grid[nr, nc])
    return adjacent_colors

def find_contiguous_object(grid, start_row, start_col, color):
    """Finds a contiguous block of the given color starting from a given cell."""
    rows, cols = grid.shape
    object_pixels = []
    visited = set()
    stack = [(start_row, start_col)]

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
            object_pixels.append((r, c))
            # Add adjacent cells to the stack
            stack.extend(get_neighbors(grid, r, c))
    return object_pixels

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Color 9 Removal
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 9:
                if any(output_grid[nr, nc] == 0 for nr, nc in get_neighbors(output_grid, r, c)):
                    output_grid[r, c] = 0

    # 2. Enclosed Object Color Transformation
    visited = set()
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and output_grid[r, c] != 0:
                color = output_grid[r, c]
                object_pixels = find_contiguous_object(output_grid, r, c, color)
                visited.update(object_pixels)

                adjacent_colors = set()
                for row, col in object_pixels:
                    adjacent_colors.update(get_adjacent_colors(output_grid, row, col))
                adjacent_colors.discard(color)
                adjacent_colors.discard(0)

                if len(adjacent_colors) == 1:
                    new_color = adjacent_colors.pop()
                    for row, col in object_pixels:
                        output_grid[row, col] = new_color

    # 3. Vertical Line Modification
    for c in range(cols):
        first_non_zero_row = -1
        for r in range(rows):
            if output_grid[r, c] != 0:
                if first_non_zero_row == -1:
                    first_non_zero_row = r
                else:
                    # Found a second non-zero pixel, change the first one.
                    output_grid[first_non_zero_row, c] = 0
                    break  # Stop searching in this column


    return output_grid.tolist()