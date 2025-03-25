```python
"""
1.  **Identify Objects:** Locate all contiguous blocks of green (3) and red (2) pixels within the input grid.

2.  **Find Start:** Determine the top-leftmost green pixel. This pixel serves as the origin point for the transformation.

3. **Output Shape**: The output width is always 7, the height is always 4

4.  **Create Gray Diagonal:** Starting from the top-left green pixel, create a diagonal line of gray (5) pixels extending downwards and to the right.  The length of the diagonal appears to be linked to how many columns to the right a red pixel exists from the starting green pixel.

5. **Conditional Red Replacement:** Red pixels are replaced by gray *only* if they fall on a diagonal down and to the right of *any* green pixel.

6. **Background:** Fill all other cells in the output grid with white (0).

7. **Cropping/Resizing:** The final output grid may be a cropped or resized version of the initial grid. The output is consistently 4x7 across the examples. The right most column of the transformed image seems to correlate to the difference in the starting columns of the leftmost green and leftmost red pixel
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of a given color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((4,7), dtype=int)  # Fixed output size

    # find green and red objects
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)
    
    # flatten into pixel lists
    green_pixels = [pixel for obj in green_objects for pixel in obj]
    red_pixels = [pixel for obj in red_objects for pixel in obj]

    # find top-left green
    if (len(green_pixels) > 0):
      green_pixels.sort()
      start_r, start_c = green_pixels[0]

      # iterate through all green pixels
      for green_r, green_c in green_pixels:
        # create diagonals from each, replacing green along the way
        for i in range(min(4 - green_r, 7- green_c)):
            current_r = green_r + i
            current_c = green_c + i

            if (current_r < 4):
                output_grid[current_r, current_c] = 5

            # Conditional Red Replacement within bounds
            for red_r, red_c in red_pixels:
                if red_r == current_r and red_c == current_c :
                  output_grid[red_r, red_c] = 5

    return output_grid
```