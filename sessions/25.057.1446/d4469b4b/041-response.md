# d4469b4b • 041 • refine_coder

---
```python
"""
1.  **Identify Seed:** Locate the green pixel(s) in the input grid. These are the "seed" points.
2.  **Identify Target Region:** Find all white pixels that form a contiguous region, *including diagonal*, connected to, or surrounding, the green seed pixel(s).
3.  **Expansion:** Change all pixels within the identified white region to green.
"""

import numpy as np
from scipy.ndimage import label

def find_pixels_by_color(grid, color):
    return np.array(np.where(grid == color)).T

def flood_fill(grid, start_coords, target_color, fill_color):
    """
    Flood fills a region of the grid with the given fill color, starting at seed_coords.

    Args:
        grid: A numpy array representing the image.
        seed_coords: A list of (row, col) tuples representing the starting coordinates.
        target_color: The color of pixels to be replaced.
        fill_color: The new color to fill the region with.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    
    # Convert start_coords to a list of tuples if it's a NumPy array
    start_coords = [tuple(coord) for coord in start_coords]
    
    stack = start_coords

    while stack:
        row, col = stack.pop()

        if (0 <= row < rows and 0 <= col < cols and
            grid[row, col] == target_color and not visited[row, col]):
            
            grid[row, col] = fill_color
            visited[row, col] = True

            # Add all 8 neighbors (including diagonals)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    stack.append((row + dr, col + dc))
    return grid


def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find green pixels (seeds)
    green_pixels = find_pixels_by_color(output_grid, 3)

    # Find white pixels (target region for expansion)
    white_pixels = find_pixels_by_color(output_grid, 0)
    if len(white_pixels) == 0:
      return output_grid
    
    white_coords_list = [tuple(coord) for coord in white_pixels]

    # Expand from each green pixel to fill connected white regions.
    output_grid = flood_fill(output_grid, white_coords_list, 0, -1) #Mark white with -1.
    for r, c in green_pixels:
      output_grid[r,c] = -1 #mark greens.
        
    output_grid = flood_fill(output_grid, [(r,c) for r, c in green_pixels], -1, 3)

    return output_grid
```
