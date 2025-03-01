# 794b24be • 012 • refine_coder

---
```python
"""
1.  **Initialization:** Start with a copy of the input grid as the output grid.

2.  **First Row Transformation:** Identify all blue pixels (value 1) in the first row of the input grid. Change these pixels to red (value 2) in the output grid.

3.  **Iterative Propagation:**
    *   Iteratively, until no more changes occur:
        *   Find all blue pixels in the input grid that are neighbors (orthogonal or diagonal) of red pixels in the output grid.
        *   Change those blue pixels to red in the output grid.

4.  **Final Output:** The output grid now represents the transformed image. All other pixels remain their original color.
"""

import numpy as np

def get_neighbors(grid, row, col):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                neighbors.append((r, c))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # First pass for first-row blue pixels
    for col in range(cols):
        if input_grid[0, col] == 1:
            output_grid[0, col] = 2

    # Iterative propagation
    while True:
        changed = False
        new_output_grid = np.copy(output_grid)  # Work on a copy to avoid immediate feedback
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] == 1 and output_grid[r,c] != 2: # blue in input, not yet red
                    neighbors = get_neighbors(output_grid, r, c)
                    for nr, nc in neighbors:
                        if output_grid[nr, nc] == 2:  # If any neighbor is red
                            new_output_grid[r,c] = 2   # change to red
                            changed = True
                            break  # Inner loop break - pixel changed
        
        if not changed:
            break

        output_grid = new_output_grid

    return output_grid
```

