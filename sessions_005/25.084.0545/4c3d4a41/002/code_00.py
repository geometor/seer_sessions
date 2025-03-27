import numpy as np

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