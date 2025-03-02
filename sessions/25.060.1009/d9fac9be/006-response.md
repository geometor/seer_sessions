# d9fac9be • 006 • refine_coder

---
```python
"""
1. Identify and Count Discontiguous Red Pixels: Examine the input grid and count only the *discontiguous single pixels* that are red (value 2). Ignore red regions of any other shape.
2. Determine Output Grid Size: The output grid will be a square grid of size N x N, where N is the number of discontiguous single red pixels counted in step 1.
3. Create Output Grid: Create an N x N grid filled entirely with white pixels (value 0).
"""

import numpy as np

def count_discontiguous_red_pixels(grid):
    """Counts the number of discontiguous single red pixels in a grid."""
    count = 0
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 2 and not visited[i, j]:
                # Check if it's a single pixel region
                is_single = True
                for x in range(max(0, i - 1), min(rows, i + 2)):
                    for y in range(max(0, j - 1), min(cols, j + 2)):
                        if (x != i or y != j) and grid[x, y] == 2:
                            is_single = False
                            break
                    if not is_single:
                        break

                if is_single:
                    count += 1

                # Mark connected component as visited (even though we only want singles)
                if grid[i, j] == 2:
                    stack = [(i,j)]
                    while stack:
                        r, c = stack.pop()
                        if 0 <= r < rows and 0 <= c < cols and grid[r,c] == 2 and not visited[r,c]:
                            visited[r, c] = True
                            for x in range(max(0, r - 1), min(rows, r + 2)):
                                for y in range(max(0, c - 1), min(cols, c + 2)):
                                     stack.append((x,y))

    return count

def transform(input_grid):
    # Count discontiguous single red pixels
    count = count_discontiguous_red_pixels(np.array(input_grid))

    # Create an N x N output grid filled with white pixels
    output_grid = np.zeros((count, count), dtype=int)

    return output_grid
```
