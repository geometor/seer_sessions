```python
"""
Replaces all instances of '5' in the input grid with a sequence of numbers
starting from 1. The sequence resets for each contiguous block of '5's,
prioritizing replacement from top-left to bottom-right.
"""

import numpy as np

def get_contiguous_blocks(grid, value):
    """
    Finds contiguous blocks of a given value in the grid.
    Returns a list of bounding box represented as ((row_min, col_min), (row_max, col_max)).
    Prioritizes top-left blocks.
    """
    blocks = []
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == value and not visited[r, c]:
                block = []
                stack = [(r, c)]
                visited[r, c] = True
                min_row, max_row = r, r
                min_col, max_col = c, c

                while stack:
                    curr_r, curr_c = stack.pop()
                    block.append((curr_r, curr_c))
                    min_row = min(min_row, curr_r)
                    max_row = max(max_row, curr_r)
                    min_col = min(min_col, curr_c)
                    max_col = max(max_col, curr_c)

                    # Check adjacent cells
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if 0 <= new_r < grid.shape[0] and 0 <= new_c < grid.shape[1] and \
                           grid[new_r, new_c] == value and not visited[new_r, new_c]:
                            stack.append((new_r, new_c))
                            visited[new_r, new_c] = True
                blocks.append( ((min_row, min_col), (row_max, max_col)))

    # Sort the blocks based on top-left priority (min_row ascending, min_col ascending).
    blocks.sort(key=lambda x: (x[0][0], x[0][1]))

    return blocks

def transform(input_grid):
    """
    Transforms the input grid by replacing 5s with a sequence of numbers.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    output_grid = np.copy(input_grid)
    replacement_sequence = 1

    blocks = get_contiguous_blocks(input_grid, 5)

    for block in blocks:
      for r in range(block[0][0], block[1][0] + 1):
        for c in range(block[0][1], block[1][1] + 1):
            if output_grid[r,c] == 5:
              output_grid[r,c] = replacement_sequence
      replacement_sequence += 1

    return output_grid
```