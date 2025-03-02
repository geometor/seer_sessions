# dbc1a6ce • 002 • example_4 • investigate_coder

---
```python
"""
Identifies blue pixels (1) in the input grid and connects them with azure pixels (8) using horizontal and vertical lines. Azure pixels fill empty cells (0s) that are on a straight line connecting the blue cells, and a single azure pixel appears adjacent to each blue cell.
"""

import numpy as np

def get_blue_pixels(grid):
    # Find coordinates of blue pixels
    return np.argwhere(grid == 1)

def transform(input_grid):
    """Transforms the input grid by connecting blue pixels with azure lines."""
    output_grid = np.copy(input_grid)
    blue_pixels = get_blue_pixels(input_grid)

    # Iterate through all pairs of blue pixels
    for i in range(len(blue_pixels)):
        for j in range(i + 1, len(blue_pixels)):
            x1, y1 = blue_pixels[i]
            x2, y2 = blue_pixels[j]

            # Check if they are on the same row or column
            if x1 == x2:  # Same column
                for y in range(min(y1, y2) + 1, max(y1, y2)):
                    if output_grid[x1, y] == 0:
                        output_grid[x1, y] = 8
            elif y1 == y2:  # Same row
                for x in range(min(x1, x2) + 1, max(x1, x2)):
                    if output_grid[x, y1] == 0:
                        output_grid[x, y1] = 8

    # Ensure at least one adjacent azure pixel
    for x, y in blue_pixels:
       
        neighbors = []
        if x > 0: neighbors.append((x-1,y))
        if x < output_grid.shape[0] - 1: neighbors.append((x+1, y))
        if y > 0: neighbors.append((x, y-1))
        if y < output_grid.shape[1] - 1: neighbors.append((x, y+1))

        has_adjacent_azure = False
        for nx, ny in neighbors:
            if output_grid[nx, ny] == 8:
                has_adjacent_azure = True
                break
        if not has_adjacent_azure:
            for nx, ny in neighbors:
                if output_grid[nx,ny] == 0:
                    output_grid[nx,ny] = 8
                    break
    return output_grid
```
