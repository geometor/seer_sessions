# db3e9e38 • 006 • refine_coder

---
```python
"""
1.  **Identify Orange Pixels:** Locate all orange (7) pixels within the input grid.
2.  **Transform Adjacent Pixels:** For *each* orange pixel:
    *   Change the color of all directly adjacent pixels (up, down, left, right, and diagonally) to azure (8).
3.  **Wrap-Around:** If an orange pixel is located on the edge of the grid, apply the transformation to the corresponding pixels on the opposite edge (e.g., a pixel adjacent to the top edge affects the bottom edge).
4.  **Preserve Source**: Orange pixels at the *source* positions are not changed, unless they become adjacent to another orange source pixel as a consequence of the transformation.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Find all orange pixels (source positions).
    orange_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 7:
                orange_pixels.append((r, c))

    # Iterate through orange pixels and transform adjacent pixels to azure.
    for r, c in orange_pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the orange pixel itself

                nr, nc = r + dr, c + dc

                # Wrap around logic
                if nr < 0:
                    nr = rows - 1
                elif nr >= rows:
                    nr = 0

                if nc < 0:
                    nc = cols - 1
                elif nc >= cols:
                    nc = 0

                output_grid[nr, nc] = 8

    return output_grid
```

