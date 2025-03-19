# d22278a0 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Create a Checkerboard:** Generate a checkerboard pattern on the 12x12 grid, alternating between 3 (green) and 0 (white) cells, starting with 3 (green) in the top left corner. A cell contains a 3, if the sum of its row and col is even, else it is 0.

2.  **Flood Fill Azure (8):** Starting from the initial 8 (azure) cell in the bottom left corner of the input, flood fill outwards. The flood fill should only replace 0 (white) cells. It is blocked by and therefore does not replace, the 3 (green) cells of the checkerboard. The fill extends diagonally.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Create Checkerboard
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 0:
                output_grid[r, c] = 3

    # Find initial azure cell
    azure_start = None
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                azure_start = (r, c)
                break
        if azure_start:
            break

    # Flood Fill Azure
    if azure_start:
        queue = [azure_start]
        while queue:
            r, c = queue.pop(0)
            if output_grid[r, c] == 0:
                output_grid[r, c] = 8
                # Add neighbors to queue
                if r + 1 < rows:
                    queue.append((r + 1, c))
                if r - 1 >= 0:
                    queue.append((r - 1, c))
                if c + 1 < cols:
                    queue.append((r, c + 1))
                if c - 1 >= 0:
                    queue.append((r, c - 1))
                if r + 1 < rows and c + 1 < cols:
                        queue.append((r+1, c+1))
                if r - 1 >= 0 and c - 1 >= 0:
                    queue.append((r - 1, c - 1))
                if r + 1 < rows and c - 1 >= 0:
                    queue.append((r+1, c - 1))
                if r - 1 >= 0 and c + 1 < cols:
                    queue.append((r-1, c+1))


    return output_grid
```
