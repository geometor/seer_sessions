# 6d58a25d • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all objects, defined as contiguous blocks of pixels of the same color (excluding 0, the background). Focus on objects of colors 8 (azure), 9 (maroon), 2(red), 7(orange), 3(green), and 4(yellow).

2.  **Extend/Replace:**
    *   If there's a "maroon" (color 9) object. Extend color 8 (azure) downwards, starting from every color 8 in the original and replacing every 9 by an 8.
    *  If there's a "red" (color 2) object. Extend it with color 2 (red) downwards, starting from every color 2 in the original and replacing every 7 by 2.
    * If there's a "green" (color 3) object that is not adjacent with a color 4. Extend the color 3 downwards. If a color 3 pixel has adjacent color 4, replace color 3 with color 4 and preserve color 4.

3.  **Preserve Background:** The white background (color 0) remains unchanged.

4. **Other colors**: copy them to the output
"""

import numpy as np

def get_objects(grid):
    """
    Finds contiguous objects of the same color in the grid.
    Returns a dictionary of objects, where keys are colors and values are lists of coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and (r, c) not in visited:
                obj_coords = []
                dfs(r, c, color, obj_coords)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def is_adjacent(coord1, coord2):
    """Checks if two coordinates are adjacent (horizontally or vertically)."""
    r1, c1 = coord1
    r2, c2 = coord2
    return (abs(r1 - r2) == 1 and c1 == c2) or (abs(c1 - c2) == 1 and r1 == r2)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    objects = get_objects(input_grid)

    # Extend/Replace for color 8 and 9
    if 8 in objects and 9 in objects:
      for azure_coords in objects[8]:
        for r_az, c_az in azure_coords: # iterate all initial positions of 8
          for r in range(r_az + 1, rows):
            if output_grid[r, c_az] == 9:
              output_grid[r, c_az] = 8
            else: # stop if not 9
              break

    # Extend/Replace for color 2 and 7
    if 2 in objects and 7 in objects:
        for red_coords in objects[2]:
          for r_red, c_red in red_coords:
            for r in range(r_red + 1, rows):
              if output_grid[r,c_red] == 7:
                output_grid[r, c_red] = 2
              else:
                break


    # Extend/replace for color 3 and 4.
    if 3 in objects:
        for green_coords in objects[3]:
            for r_g, c_g in green_coords:
                has_adjacent_4 = False
                for r in range(max(0, r_g - 1), min(rows, r_g + 2)):
                  for c in range(max(0, c_g -1), min(cols, c_g + 2)):
                    if (r,c) != (r_g, c_g) and input_grid[r,c] == 4:
                      has_adjacent_4 = True
                      break
                  if has_adjacent_4:
                    break

                if has_adjacent_4: # replace 3 by 4
                  output_grid[r_g, c_g] = 4
                else:  #extend 3
                  for r in range(r_g+1, rows):
                    if output_grid[r, c_g] == 0:
                      output_grid[r,c_g] = 3
                    else:
                      break
    return output_grid
```
