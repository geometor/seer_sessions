# 09629e4f • 014 • refine_coder

---
```python
"""
1.  **Background:** The output grid is initialized with a background of gray (color code 5).

2.  **Component Identification:** Identify all connected components within the input grid.  A connected component is a group of orthogonally adjacent pixels (up, down, left, right – not diagonally) that share the same color.

3.  **Expansion Rule:**
    *   If a connected component has more than one pixel, expand each pixel in that component into a 3x3 block of the same color in the output grid. The 3x3 block is centered on the pixel's original location.
    * If parts of the 3x3 block would extend past the edges of the grid, the expansion stays within bounds.
    * Only update output cells that are still the default background color.

4.  **Singular Pixel Rule:** If a pixel is *not* part of a connected component (i.e., it is an isolated pixel with a component size of 1), set its corresponding pixel in the output grid to gray (5).

5. **Output** Return the final output grid.
"""

import numpy as np
from collections import deque

def get_connected_component(grid, start_row, start_col, color):
    """Finds a connected component of a given color using Breadth-First Search (BFS)."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    queue = deque([(start_row, start_col)])
    component = []

    while queue:
        row, col = queue.popleft()
        if (0 <= row < rows and 0 <= col < cols and
                grid[row, col] == color and not visited[row, col]):
            visited[row, col] = True
            component.append((row, col))
            # Add orthogonal neighbors
            queue.append((row + 1, col))
            queue.append((row - 1, col))
            queue.append((row, col + 1))
            queue.append((row, col - 1))
    return component

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""

    rows, cols = input_grid.shape
    output_grid = np.full((rows, cols), 5)  # Initialize with gray (5)

    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] != 5:
                # Connected Component Check
                component = get_connected_component(input_grid, i, j, input_grid[i, j])

                if len(component) > 1:
                    # Expansion
                    for r, c in component:
                        for x in range(max(0, r - 1), min(rows, r + 2)):
                            for y in range(max(0, c - 1), min(cols, c + 2)):
                                if output_grid[x, y] == 5:  # Only update if it's background
                                    output_grid[x, y] = input_grid[r, c]
                else:
                    # Singular Pixel Handling
                    output_grid[i, j] = 5

    return output_grid
```
