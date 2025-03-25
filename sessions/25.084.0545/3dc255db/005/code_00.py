"""
1.  **Color 9 Removal:**
    *   Iterate through each cell in the grid.
    *   If a cell has a color value of 9:
        *   Check its immediate left and right neighbors.
        *   If *either* the left or right neighbor is a non-zero, non-9 color, change the cell's color to 0.

2.  **Enclosed Object Color Transformation:**
    * Identify all contiguous objects (blocks of the same non-zero color).
    * For each object, find colors adjacent to it.
    * If an object borders *only* color 0 and one other color, the object changes to the other color.
    * Exclude the object color from the adjacency list

3. **Vertical Line Modification**
    * Scan columns from left to right.
    * For each column:
       * Find the top-most non-zero color.
       * If there's *any* other non-zero color *below* it in the same column, change the top-most color to 0.
"""

import numpy as np

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
            stack.append((r + 1, c))
            stack.append((r - 1, c))
            stack.append((r, c + 1))
            stack.append((r, c - 1))
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
                adjacent_colors = get_adjacent_colors(input_grid, r, c)
                if any(color != 0 and color != 9 for color in adjacent_colors):
                    if (c > 0 and input_grid[r,c-1] != 0 and input_grid[r,c-1] !=9 ) or (c < cols-1 and input_grid[r,c+1] !=0 and input_grid[r,c+1] != 9):
                        output_grid[r, c] = 0

    # 2. Enclosed Object Color Transformation
    visited = set()
    for r in range(rows):
        for c in range(cols):
            if (r,c) not in visited and output_grid[r,c] != 0:
                color = output_grid[r,c]
                block = find_contiguous_object(output_grid, r, c, color)
                visited.update(block)

                adjacent_block_colors = set()
                for br,bc in block:
                    adjacent_block_colors.update(get_adjacent_colors(output_grid, br, bc))

                adjacent_block_colors.discard(color)
                if len(adjacent_block_colors) == 1:
                    adj_color = adjacent_block_colors.pop()
                    if adj_color != 0:
                        bordering = set()
                        for br,bc in block:
                            bordering.update(get_adjacent_colors(output_grid, br,bc))
                        if all(x == adj_color or x==0 for x in bordering if x != color):
                            for (br, bc) in block:
                                output_grid[br, bc] = adj_color

    # 3. Vertical Line Modification
    for c in range(cols):
        first_color = 0
        first_color_row = -1
        for r in range(rows):
            if output_grid[r, c] != 0:
                if first_color == 0:
                    first_color = output_grid[r, c]
                    first_color_row = r
                elif first_color != output_grid[r, c]:
                    first_color = -1  # Signal to stop
                    break # added break

        if first_color > 0:
            output_grid[first_color_row, c] = 0


    return output_grid.tolist()