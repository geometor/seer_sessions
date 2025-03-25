```python
"""
The task is to identify and extract the largest square subgrid within the input grid that has a uniform non-zero color, potentially bordered by zeros.
"""

import numpy as np

def find_largest_uniform_square(grid):
    """
    Finds the largest square subgrid within the input grid with a uniform non-zero color, including bordering zeros.
    """
    rows, cols = grid.shape
    max_size = 0
    top_left = (0, 0)
    target_color = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                color = grid[r, c]
                for size in range(1, min(rows - r, cols - c) + 1):
                    valid_square = True
                    for i in range(r, r + size):
                        for j in range(c, c + size):
                            if grid[i, j] != 0 and grid[i, j] != color:
                                valid_square = False
                                break
                        if not valid_square:
                            break
                    if valid_square:
                        if size > max_size:
                            max_size = size
                            top_left = (r, c)
                            target_color = color
                    else:
                        break  # Optimization: If a square is invalid, no larger square starting here will work

    return top_left, max_size, target_color

def transform(input_grid):
    """
    Transforms the input grid by extracting the largest square subgrid of uniform color, including bordering zeros.
    """
    input_grid = np.array(input_grid)
    
    # Find the largest uniform square subgrid.
    top_left, size, color = find_largest_uniform_square(input_grid)

    if size == 0:
      return []
    # Extract the subgrid.
    output_grid = input_grid[top_left[0]:top_left[0] + size, top_left[1]:top_left[1] + size]

    return output_grid.tolist()
```