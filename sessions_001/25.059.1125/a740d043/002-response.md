# a740d043 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify Non-Blue Objects: Examine the input grid and locate all contiguous blocks of pixels that are *not* blue (value 1). These blocks can be of any shape and color other than blue.
2. Consider White Objects: Examine if the output grid includes white colored pixels (value 0). White pixels might be included between the extracted objects.
3. Create Output Grid: Create a new, smaller grid. The dimensions of this grid are not fixed but are determined by the arrangement of the identified non-blue (and possibly white) objects.
4. Populate Output Grid: Transfer the non-blue (and white) objects from the input grid to the output grid, maintaining the original shape/colors of each extracted parts. Arrange those parts such that any gaps between the non-blue pixels in the input are closed.

In simple terms: the input shows some non-blue clusters surrounded by blue. Copy all non-blue clusters to a smaller plate, discarding all blue pixels (and maybe keeping white ones), and make a new figure using copied clusters.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of non-blue pixels in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 1:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects
                
def check_white_inclusion(examples):
   """Check training data to see if any output grids includes white pixels (value 0).
      Return True if white is present, false otherwise.
   """
   for example in examples:
       if 0 in example['output']:
            return True
   return False
                

def transform(input_grid, examples):
    """Transforms the input grid according to the identified rule."""
    
    # identify if 0 should be kept or not
    keep_white = check_white_inclusion(examples)

    # Find non-blue objects
    objects = find_objects(input_grid)
    
    # Create a list to store the values and coordinates of object pixels.
    output_pixels = []

    # Extract and store pixel values
    for obj in objects:
        for r, c in obj:
            output_pixels.append((grid[r,c],r,c))

   # find dimensions and offset for the output pixels

    if len(output_pixels) == 0:
        return np.array([[]]) # Return empty grid if no non blue pixels

    min_r = min(pixel[1] for pixel in output_pixels)
    min_c = min(pixel[2] for pixel in output_pixels)

    max_r = max(pixel[1] for pixel in output_pixels)
    max_c = max(pixel[2] for pixel in output_pixels)

    # calculate height and width based on position of pixels
    height = 0
    width = 0

    pixel_positions = []

    for value, r, c in output_pixels:
        new_r = r - min_r
        new_c = c - min_c

        height = max(height, new_r + 1) # at least 1
        width = max(width, new_c + 1) # at least 1

        pixel_positions.append((value, new_r, new_c))
        
    # Initialize output grid
    output_grid = np.zeros((height, width), dtype=int)

    # Populate output grid with the values extracted from the objects
    for value, r, c in pixel_positions:
        output_grid[r, c] = value
    return output_grid
```
