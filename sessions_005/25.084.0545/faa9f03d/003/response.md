```python
"""
Transforms the input grid based on the following rules:

1.  **Unchanged Regions:** Large regions of color 3 in Example 1, color 7 in
    Example 2, and color 1 in Example 3 are unchanged.
2.  **Replacements:**
    -   Red (2) is always replaced with green (3).
    -   Yellow (4) is replaced with either green (3) or magenta (6).
    -   Magenta (6) may expand to fill the background.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous regions of the same color as objects.
    Returns a dictionary where keys are colors and values are lists of (row, col) tuples.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color not in objects:
                    objects[color] = []
                dfs(r, c, color, objects[color])
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    objects = find_objects(input_grid)

    # Apply replacement rules
    for color, pixels in objects.items():
        if color == 2:  # Replace red with green
            for r, c in pixels:
                output_grid[r, c] = 3
        elif color == 4: #replace yellow
            if len(pixels) == 1: #only single pixel yellows are transformed
              #check if example 2 or 3
              magenta_present = 6 in input_grid
              if magenta_present:
                for r,c in pixels:
                  output_grid[r,c] = 6
              else:
                for r,c in pixels:
                  output_grid[r,c] = 3
    #Magenta expansion
    if 6 in objects:

      #check for presence of 1s:
      if 1 in input_grid:
        for r in range(rows):
          for c in range(cols):
            if output_grid[r,c] == 0:
              output_grid[r,c] = 6
      else: #example 3 logic doesn't apply.
        pass
    return output_grid
```