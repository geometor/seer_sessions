"""
1.  **Identify Objects:** Scan the input grid and identify all distinct objects. An object is a group of connected pixels of the same color. Connectivity is defined by shared sides (not diagonals).

2.  **Identify the largest connected component by color.**
    For each distinct, non-background (non-zero) color: Find the largest connected area of that color.

3.  **Remove color 9 (maroon) objects.**
    Scan the input for distinct, non-background (non-zero) color: Remove color if all the connected component contains any color 9.

4. **Preserve Largest Components and remove others**
   - Preserve the connected components
   - If a non-background pixel is not part of its largest connected, remove by setting to 0.

5.  **Output:** The output grid is the result of applying steps 2 & 3.
"""

import numpy as np
from collections import defaultdict

def get_connected_components(grid):
    """Finds connected components in a grid."""
    visited = set()
    components = defaultdict(list)

    def dfs(r, c, color, component_id):
        if (r, c) in visited or not (0 <= r < len(grid) and 0 <= c < len(grid[0])) or grid[r, c] != color:
            return
        visited.add((r, c))
        components[component_id].append((r, c))
        dfs(r + 1, c, color, component_id)
        dfs(r - 1, c, color, component_id)
        dfs(r, c + 1, color, component_id)
        dfs(r, c - 1, color, component_id)

    component_id = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) not in visited and grid[r, c] != 0:
                dfs(r, c, grid[r, c], component_id)
                component_id += 1
    return components

def get_largest_component_by_color(components, grid):
   """Returns a dictionary of largest components for each color."""
   largest_components = {}
   for component_id, pixels in components.items():
     color = grid[pixels[0][0], pixels[0][1]]
     if color not in largest_components or len(pixels) > len(largest_components[color]):
        largest_components[color] = pixels
   return largest_components

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    components = get_connected_components(grid)

    #remove all maroon (9)
    for r in range(len(grid)):
      for c in range(len(grid[0])):
        if grid[r,c] == 9:
          output_grid[r,c] = 0

    components = get_connected_components(output_grid) #update after removing maroon

    largest_components = get_largest_component_by_color(components, output_grid)

    #remove pixels from secondary same color components
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            color = grid[r, c]
            if color != 0:
                found_in_largest = False
                if color in largest_components:
                  for lr, lc in largest_components[color]:
                    if lr == r and lc == c:
                      found_in_largest = True
                      break
                if not found_in_largest:
                  output_grid[r,c] = 0

    return output_grid.tolist()