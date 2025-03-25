"""
Identifies the largest connected group of red pixels ('2') above a yellow separator line ('4') in a grid, and creates a new grid containing only the bounding box of this transformed blob, where the red pixels are changed to green ('3').
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Returns the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def dfs(grid, row, col, visited, blob):
    """Performs Depth-First Search to find connected components."""
    if (row, col) in visited or grid[row, col] != 2:
        return
    visited.add((row, col))
    blob.append((row, col))
    for neighbor_row, neighbor_col in get_neighbors(grid, row, col):
        dfs(grid, neighbor_row, neighbor_col, visited, blob)

def find_largest_blob_above_separator(grid):
    """Finds the largest connected blob of '2's above the separator row."""
    separator_row_index = -1
    for i in range(grid.shape[0]):
        if 4 in grid[i]:
            separator_row_index = i
            break

    if separator_row_index == -1:
        return []  # No separator found

    visited = set()
    blobs = []
    for row in range(separator_row_index):
        for col in range(grid.shape[1]):
            if grid[row, col] == 2 and (row, col) not in visited:
                blob = []
                dfs(grid, row, col, visited, blob)
                blobs.append(blob)

    if not blobs:
        return []

    max_size = max(len(blob) for blob in blobs)
    largest_blobs = [blob for blob in blobs if len(blob) == max_size]
    return largest_blobs[0] if largest_blobs else [] # Return only one, even if multiple of same size

def transform(input_grid):
    """Transforms the input grid according to the problem rules."""
    # 1. Find Separator
    separator_row_index = -1
    for i in range(input_grid.shape[0]):
        if 4 in input_grid[i]:
            separator_row_index = i
            break

    if separator_row_index == -1:
        return np.array([])  # Return empty array if no separator

    # 2. Identify Red Blobs Above Separator & 3. Find the Largest Red Blob
    largest_blob = find_largest_blob_above_separator(input_grid)

    if not largest_blob:
      return np.array([]) # Return empty array if no blob

    # 4. Create Output Grid (Bounding Box)
    min_row = min(row for row, _ in largest_blob)
    max_row = max(row for row, _ in largest_blob)
    min_col = min(col for _, col in largest_blob)
    max_col = max(col for _, col in largest_blob)

    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # 5. Transform Largest Blob (and copy relevant input data)
    for r, c in largest_blob:
      output_grid[r-min_row,c-min_col] = 3

    for r in range(min_row,max_row + 1):
      for c in range(min_col, max_col + 1):
        if (r,c) not in largest_blob:
          output_grid[r - min_row, c-min_col] = input_grid[r,c]


    # 6. Return output grid
    return output_grid