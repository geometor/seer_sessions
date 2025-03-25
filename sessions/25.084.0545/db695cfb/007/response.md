```python
"""
1.  **Identify Background:** Find the most frequent color in the input grid. This is the background color.
2.  **Identify Objects:**
    *   Locate all contiguous regions (connected horizontally or vertically) of non-background color. Each region is a distinct object.
    *   Record the initial positions and color of each object.
3.  **Check for Single Object and Shift Condition**:
    *  Count object locations.
    *  If a single color is present in the input grid, and its number of start locations is less than or equal to two, then perform a vertical shift:
      *  Move the entire object upwards (as a unit) in the grid until a non-background pixel is adjacent vertically to another non-background pixel, or the object has reached the top row.
4.  **Expansion (if not shifted):** If shift condition is not met (i.e. more than 1 object, or a single object with more than 2 start locations), perform iterative cross expansion:
    *   Iterate through each object's pixels.  For each pixel:
        *   Expand the object's color into all adjacent (up, down, left, right) background pixels.
        *   If multiple objects try to expand into the same background pixel:
            *   If one of the competing colors is 6 and another is 1, color 6 overwrites color 1.
            *   Other interactions are not defined by the given examples, so apply no change.
        * repeat expansion until no pixels change.
5.  **Output:** Return the final grid after either shifting or expansion.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    return color_counts.most_common(1)[0][0]

def find_objects(grid, background_color):
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = {}

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, object_pixels):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        dfs(r + 1, c, color, object_pixels)
        dfs(r - 1, c, color, object_pixels)
        dfs(r, c + 1, color, object_pixels)
        dfs(r, c - 1, color, object_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                object_pixels = []
                dfs(r, c, color, object_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(object_pixels)
    return objects

def shift_object(grid, object_pixels, color, background_color):
    # shift object up
    rows, cols = grid.shape
    min_row = min(r for r, c in object_pixels)
    height = max(r for r, c in object_pixels) - min_row + 1
    new_grid = np.full(grid.shape, background_color, dtype=grid.dtype)

    # Calculate the shift amount, preventing out-of-bounds access
    shift = min_row

    # Copy object to new location
    for r, c in object_pixels:
        new_grid[r-shift,c] = color
        
    return new_grid

def expand_object(grid, object_pixels, color, background_color):
    new_pixels = set()
    rows, cols = grid.shape
    for r, c in object_pixels:
      #Check neighbors and add them to new_pixels if they are background
      neighbors = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
      for nr, nc in neighbors:
          if 0 <= nr < rows and 0 <= nc < cols and grid[nr,nc] == background_color:
              new_pixels.add((nr,nc))

    return new_pixels

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify the Background
    background_color = get_background_color(input_grid)

    # 2. Identify Objects
    objects = find_objects(input_grid, background_color)
    
    # 3. Construct Output Grid (initialize with background)
    output_grid = np.full(input_grid.shape, background_color, dtype=input_grid.dtype)

    # Check for single object and shift condition
    if len(objects) == 1 and sum(len(obj) for obj in objects.values()) <= 2:
        color = list(objects.keys())[0]
        # shift only one object
        object_pixels = objects[color][0]  # Assuming single object
        output_grid = shift_object(input_grid, object_pixels, color, background_color)
    else:
        # 4. Expansion
       
        # first copy initial object locations
        output_grid = np.copy(input_grid)

        while True:
            new_pixels_to_add = {} # (r,c) : color
            
            # gather new pixels from each object
            all_objects = find_objects(output_grid, background_color)
            for color, object_instances in all_objects.items():
                for object_pixels in object_instances:
                    expanded_pixels = expand_object(output_grid, object_pixels, color, background_color)
                    for r,c in expanded_pixels:
                        if (r,c) not in new_pixels_to_add:
                            new_pixels_to_add[(r,c)] = color
                        else:
                            # color interactions
                            if color == 6 and new_pixels_to_add[(r,c)] == 1:
                                new_pixels_to_add[(r,c)] = 6
                            elif color == 1 and new_pixels_to_add[(r,c)] == 6:
                                 new_pixels_to_add[(r,c)] = 6 # 6 wins
                                

            if not new_pixels_to_add:
              break

            # Apply changes, handle collision
            for (r,c), color in new_pixels_to_add.items():
                output_grid[r,c] = color
                
    return output_grid.tolist()
```