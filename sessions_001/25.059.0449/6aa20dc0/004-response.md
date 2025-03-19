# 6aa20dc0 • 004 • refine_coder

---
```python
"""
1.  **Identify Objects:** Determine all contiguous regions (objects) of the same color within the input grid.
2.  **Identify Background:** Identify the background color. The background color does not change.
3.  **Object Interaction:**
    *   Objects of color red expand. If the background is blue, the red object expands to the *right* and fills with azure; If the background is yellow, the red object expands to the *left* and fills with red.
    *   Objects of color green expand.  If the background is blue, the green object expands to the *left* and fills with azure. If the background is azure, the green object expands to the *left* and fills with green.
    * Objects of color magenta expand to the *left* and fills with the same color when the background is yellow.
    * Other colored objects do not change.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(r, c, color, obj_pixels):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_pixels.append((r, c))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, color, obj_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c]:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects


def get_background_color(grid, objects):
    """
    Determine the most frequent color, which is assumed to be the background.
    """
    all_pixels = set()
    for r in range(grid.shape[0]):
      for c in range(grid.shape[1]):
        all_pixels.add((r,c))

    object_pixels = set()
    for obj in objects:
        object_pixels.update(obj)
    
    background_pixels = list(all_pixels - object_pixels)
    if background_pixels:
      background_color = grid[background_pixels[0]]
    else:
      background_color = grid[0,0]

    return background_color


def expand_object(grid, obj_pixels, expansion_direction, expansion_color):
    """
    Expands the object by one pixel in the specified direction ('left' or 'right').
    Fills the new pixels with expansion_color
    """
    new_pixels = []
    for r, c in obj_pixels:
       if expansion_direction == 'left':
          new_pixels.append((r,c-1))
       elif expansion_direction == 'right':
          new_pixels.append((r,c+1))

    return obj_pixels + new_pixels
    

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)
    
    background_color = get_background_color(input_grid, objects)


    # change background - the background color stays the same
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r,c] == background_color:
               output_grid[r,c] = background_color
    
    # Process objects
    for obj_pixels in objects:
      first_pixel = obj_pixels[0]
      obj_color = input_grid[first_pixel]

      if obj_color != background_color:

        # Red object expansion
        if obj_color == 2:  # Red
            if background_color == 1:  # Blue background
                expanded_object = expand_object(input_grid, obj_pixels, 'right', 8) # Expand right, fill with azure
                for r, c in expanded_object:
                    if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                      if (r,c) not in obj_pixels:
                        output_grid[r, c] = 8
                      else:
                        output_grid[r,c] = 2
            elif background_color == 4:  # Yellow background
                expanded_object = expand_object(input_grid, obj_pixels, 'left', 2)  # Expand left, fill with red
                for r, c in expanded_object:
                    if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                        output_grid[r, c] = 2
        # Green object expansion
        elif obj_color == 3:  # Green
            if background_color == 1:  # Blue background
              expanded_object = expand_object(input_grid, obj_pixels, 'left', 8)
              for r,c in expanded_object:
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                  if (r,c) not in obj_pixels:
                    output_grid[r,c] = 8
                  else:
                    output_grid[r,c] = 3
            elif background_color == 8:  # Azure background
              expanded_object = expand_object(input_grid, obj_pixels, 'left', 3)
              for r, c in expanded_object:
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                  output_grid[r, c] = 3

        # Magenta object expansion
        elif obj_color == 6 and background_color == 4:  # Magenta, yellow background
            expanded_object = expand_object(input_grid, obj_pixels, 'left', 6)
            for r, c in expanded_object:
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                    output_grid[r, c] = 6

        # All other colors: no change
        else:
          for r,c in obj_pixels:
            output_grid[r,c] = obj_color

    return output_grid.tolist()
```
