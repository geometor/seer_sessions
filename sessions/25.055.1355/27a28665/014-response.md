# 27a28665 • 014 • example_3 • investigate_coder

---
```python
"""
1. Count the number of instances of the most frequent color other than color white (0).
2. If the count from step 1. is greater than 1, output the number of white (0) regions bound by this color.
"""

import numpy as np

def count_regions(grid, color, bounding_color):
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    count = 0

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return False

        visited[r, c] = True
        
        # Check for bounding color
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1), (r-1,c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]
        
        fully_bounded = True # Assume it is fully bounded to start
        
        for nr, nc in neighbors:
          if is_valid(nr, nc):
            if grid[nr, nc] != bounding_color and grid[nr, nc] != color:
              fully_bounded = False # Not fully bounded
            elif grid[nr, nc] == color:
              dfs(nr, nc)

        return fully_bounded

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                if dfs(r,c):
                  count += 1
    return count

def transform(input_grid):
    # Convert to numpy array
    grid = np.array(input_grid)

    # Find the most frequent color other than white (0)
    colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(colors, counts))
    
    if 0 in color_counts:
      del color_counts[0] # delete white
    
    if len(color_counts) == 0:
      return np.array([[0]])

    most_frequent_color = max(color_counts, key=color_counts.get)
    most_frequent_count = color_counts[most_frequent_color]

    # Count the number of white (0) regions surrounded by the most frequent color
    if most_frequent_count > 1:
        output_value = count_regions(grid, 0, most_frequent_color)
    else:
        output_value = 0

    return np.array([[output_value]])
```
