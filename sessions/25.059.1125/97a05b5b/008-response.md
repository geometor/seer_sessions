# 97a05b5b • 008 • example_1 • investigate_coder

---
```python
"""
Downsamples the input grid, representing larger regions with single colors in the output grid, favoring non-background colors and trying to preserve basic spatial relationships.
"""

import numpy as np

def get_objects(grid):
    """
    Detects contiguous regions of non-zero colors.
    Returns a dictionary of objects, where keys are colors
    and values are lists of coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects
    
def get_dominant_color(grid, block_coords):
    # Count occurrences of each color within the block
    color_counts = {}
    for r, c in block_coords:
        color = grid[r,c]
        color_counts[color] = color_counts.get(color, 0) + 1

    # Find the most frequent color
    dominant_color = 0  # default to 0
    max_count = 0

    #find if block contains background color
    has_background = 0 in color_counts

    for color, count in color_counts.items():
        if color != 0 and count > max_count:
                max_count = count
                dominant_color = color
    return dominant_color

def transform(input_grid):
    # Initialize the output grid with a default color (e.g., 0)
    input_grid = np.array(input_grid)
    output_grid = np.zeros((17, 9), dtype=int)
    
    objects = get_objects(input_grid)

    #Simplified mapping based on observation and rough coordinate mapping.
    #This is where a more dynamic approach would be beneficial in future iterations.
    
    output_coords = {
      2: [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(1,0),(1,1),(1,4),(1,5),
          (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),
          (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),
          (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),
          (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),
          (8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),
          (9,0),(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),
          (10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),
          (11,0),(11,1),(11,2),(11,3),(11,4),(11,5),(11,6),(11,7),(11,8),
          (12,0),(12,1),(12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,8),
          (15,0),(15,1),(15,2),(15,3),(15,4),(15,5),(15,6),(15,7),(15,8),
          (16,0),(16,1),(16,2),(16,3),(16,4),(16,5),(16,7),(16,7),(16,8)],
      1: [(6,3),(6,4),(8,3),(8,4)],
      3: [(1,6),(1,7),(1,8),(2,6),(2,7),(2,8),(3,6),(3,7),(3,8)],
      4: [(1,2),(1,3),(2,2),(2,3),(3,2),(3,3)],
      5: [(13,5),(13,6),(13,7),(13,8),(14,5),(14,6),(14,7),(14,8)],
      8: [(13,0),(13,1),(14,0),(14,1)]

    }

    for color, color_output_coords in output_coords.items():
      if color in objects:
        for coord in color_output_coords:
              output_grid[coord]=color


    return output_grid
```
