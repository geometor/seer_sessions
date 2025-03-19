# 673ef223 • 020 • refine_coder

---
```python
"""
1.  **Identify Initial Azure:** Locate all pixels that are initially colored azure (8). These are the starting points for expansion.
2.  **Expand Azure (Flood Fill):** For each initially azure pixel, perform a flood fill operation:
    *   Change contiguous white (0) pixels to azure (8), including diagonally adjacent pixels.
    *   Stop the flood fill when encountering *any* non-white pixel (1-9).
3.  **Replace with Yellow:** After the expansion, change all pixels that were *originally* azure (8) (before the expansion) to yellow (4).
4. **Preserve:** All non-white pixels retain their orginal colors.
"""

import numpy as np

def find_pixels(grid, color):
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == color:
                pixels.append((r,c))
    return pixels

def flood_fill(grid, start_row, start_col, fill_color):
    """
    Fills a contiguous region with the fill_color, stopping at any non-white color.
    Uses a queue-based breadth-first search approach, including diagonals.
    """
    rows, cols = grid.shape
    queue = [(start_row, start_col)]
    visited = set()

    while queue:
        r, c = queue.pop(0)

        if (r, c) in visited:
            continue
        visited.add((r, c))

        if not (0 <= r < rows and 0 <= c < cols):
            continue

        # Stop at any non-white color
        if grid[r, c] != 0:
            continue

        grid[r, c] = fill_color  # Fill the current cell

        # Add neighbors to the queue, including diagonals
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the current cell
                queue.append((r + dr, c + dc))


def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = input_grid.copy()

    # Identify initial azure pixels
    initial_azure_pixels = find_pixels(input_grid, 8)

    # expand azure, stopping at any non-white color
    for r,c in initial_azure_pixels:
      flood_fill(output_grid, r, c, 8)

    # place yellow where azure was originally
    for r, c in initial_azure_pixels:
        output_grid[r,c] = 4

    return output_grid
```

