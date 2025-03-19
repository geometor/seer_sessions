"""
The transformation rule involves the extraction of a single colored shape from a large grid, with the background removed. The output grid is a cropped representation of a *single* contiguous, non-zero colored object within the input grid.
"""

import numpy as np

def find_object(grid):
    # Find the bounding box of the first non-zero object in the grid.
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                color = grid[r, c]
                min_r, max_r = rows, -1
                min_c, max_c = cols, -1

                visited = set()
                stack = [(r, c)]

                while stack:
                    curr_r, curr_c = stack.pop()

                    if (curr_r, curr_c) in visited:
                        continue
                    visited.add((curr_r, curr_c))

                    if not (0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color):
                        continue

                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)
                    
                    stack.append((curr_r + 1, curr_c))
                    stack.append((curr_r - 1, curr_c))
                    stack.append((curr_r, curr_c + 1))
                    stack.append((curr_r, curr_c - 1))
                return (min_r, max_r + 1, min_c, max_c + 1), color
    return None, 0
                

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find the first non-zero object and its bounding box
    bbox, color = find_object(grid)
    
    if bbox is None:
      return []

    # Extract the object based on the bounding box
    min_r, max_r, min_c, max_c = bbox
    output_grid = grid[min_r:max_r, min_c:max_c]

    return output_grid.tolist()