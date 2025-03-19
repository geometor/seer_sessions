"""
Identifies the largest contiguous block of red pixels in the input grid. From
the bounding box of this red block, a sub-grid is extracted.  The output is a
3x3 grid, where each cell corresponds to a subsampled pixel from the
extracted sub-grid. The subsampling involves selecting pixels at regular
intervals (every other pixel) within the bounding box. If no red pixels are
found, a 3x3 grid of all zeros (white) is returned.
"""

import numpy as np

def find_largest_red_object(grid):
    # Find the largest connected component of red (2) pixels.
    rows, cols = len(grid), len(grid[0])
    visited = set()
    max_size = 0
    largest_object_coords = []

    def dfs(row, col, current_object_coords):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or grid[row][col] != 2
            or (row, col) in visited
        ):
            return 0
        visited.add((row, col))
        current_object_coords.append((row, col))
        size = 1
        size += dfs(row + 1, col, current_object_coords)
        size += dfs(row - 1, col, current_object_coords)
        size += dfs(row, col + 1, current_object_coords)
        size += dfs(row, col - 1, current_object_coords)
        return size

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2 and (r, c) not in visited:
                current_object_coords = []
                size = dfs(r, c, current_object_coords)
                if size > max_size:
                    max_size = size
                    largest_object_coords = current_object_coords
    return largest_object_coords

def transform(input_grid):
    # Find the largest connected red object.
    largest_red_object_coords = find_largest_red_object(input_grid)

    # If no red object is found, return a 3x3 grid of all zeros.
    if not largest_red_object_coords:
        return [[0] * 3 for _ in range(3)]

    # Determine the bounding box.
    min_row = min(r for r, _ in largest_red_object_coords)
    max_row = max(r for r, _ in largest_red_object_coords)
    min_col = min(c for _, c in largest_red_object_coords)
    max_col = max(c for _, c in largest_red_object_coords)

    # Calculate the dimensions of the bounding box.
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # Initialize the output grid with zeros.
    output_grid = [[0] * 3 for _ in range(3)]
    
    # Subsample from input to populate output
    for i in range(3):
        for j in range(3):
            row_index = min_row + (i * (height -1 ) // 2) if height > 1 else min_row
            col_index = min_col + (j * (width - 1) // 2) if width > 1 else min_col

            if (row_index < len(input_grid) and col_index < len(input_grid[0])
                  and input_grid[row_index][col_index] == 2):
                output_grid[i][j] = 1

    return output_grid