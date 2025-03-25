"""
1.  **Identify the Boundary:** Find the top horizontal gray (5) line.  Find the bottom irregular gray (5) shape. Together, these define the operational boundaries for each column.
2.  **Identify Objects:** Within the boundary, identify all distinct objects. An object is a contiguous group of pixels of the same color (excluding white and gray).
3.  **Shift Objects Left:** For each identified object:
    *   Determine the object's row.
    *   Determine the leftmost available position within that row, bounded by the gray boundary and other non-gray objects and move the object there.
    * Do not change shape.
"""

import numpy as np

def find_boundary_rows(grid):
    # Find the row index of the top horizontal gray line.
    top_row = -1
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            top_row = i
            break

    # Find the row indices of the bottom irregular gray shape.
    bottom_rows = []
    for i in range(len(grid) -1, top_row, -1):
        if any(pixel == 5 for pixel in grid[i]):
            bottom_rows.append(i)
        else:
            break;

    return top_row, bottom_rows

def find_objects(grid, top_row, bottom_rows):
    objects = []
    visited = set()
    rows, cols = grid.shape

    # determine bottom row for a column
    def get_bottom_row(col, bottom_rows):
        for r in bottom_rows:
            if grid[r, col] == 5:
                return r
        return rows # default to bottom

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0 and grid[r,c] != 5:
                # Check if within boundary
                bottom_row_for_col = get_bottom_row(c, bottom_rows)
                if r > top_row and r <= bottom_row_for_col:
                    object_pixels = []
                    stack = [(r, c)]
                    color = grid[r, c]

                    while stack:
                        curr_r, curr_c = stack.pop()
                        if (curr_r, curr_c) in visited:
                            continue
                        visited.add((curr_r, curr_c))

                        bottom_row = get_bottom_row(curr_c, bottom_rows)
                        if curr_r > top_row and curr_r <= bottom_row and grid[curr_r, curr_c] == color :
                            object_pixels.append((curr_r, curr_c))
                            # Add adjacent cells of the same color
                            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                nr, nc = curr_r + dr, curr_c + dc
                                if 0 <= nr < rows and 0 <= nc < cols:
                                    stack.append((nr, nc))
                    objects.append({'color': color, 'pixels': object_pixels})
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    top_boundary, bottom_boundaries = find_boundary_rows(input_grid)
    objects = find_objects(input_grid, top_boundary, bottom_boundaries)
    
    # Clear the original object positions within the boundary
    for obj in objects:
        for r, c in obj['pixels']:
            output_grid[r, c] = 0

    # Shift objects to the left
    for obj in objects:
        pixels = obj['pixels']
        # sort by column, then by row, so that we move left-most pixels first
        pixels.sort(key=lambda x: (x[1], x[0]))
        
        for r, c in pixels:
            # find the bottom boundary for this column
            bottom_row_for_col = -1
            for b_row in bottom_boundaries:
                if input_grid[b_row, c] == 5:
                  bottom_row_for_col = b_row
                  break;
            if (bottom_row_for_col == -1):
              bottom_row_for_col = rows-1

            # find left most available
            target_c = c
            while target_c > 0:
                if input_grid[r, target_c - 1] == 5 or (r > top_boundary and r <= bottom_row_for_col and output_grid[r,target_c - 1] == 0):
                    target_c -= 1
                else:
                    break

            output_grid[r, target_c] = obj['color']

    return output_grid