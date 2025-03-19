# d43fd935 • 006 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Key Objects:** Locate the 2x2 green square and all blue and magenta pixels.

2.  **Blue Pixel Extension:** The blue pixel on the top left ([0,0]) creates a horizontal line of blue pixels to its right. The blue pixel on the bottom row ([9,4]) also create a horizontal line of blue pixels. The length of both lines appears to be related to the size of the green square. In the specific example, the blue pixels extend 4 times to the right for the top-left blue pixel and zero times to the right for the bottom blue pixel. The extension rule appears to relate to a distance between a blue pixel and the green square.

3. **Magenta Pixel Movement:** The magenta pixels that are above the green square are moved one square down, except the one to the bottom left, that disappears.
"""

import numpy as np

def find_objects(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    return np.argwhere(grid == color).tolist()

def find_square(grid, color):
    """Finds a 2x2 square of the specified color and returns its top-left corner coordinates."""
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == color and grid[i + 1, j] == color and
                grid[i, j + 1] == color and grid[i + 1, j + 1] == color):
                return (i, j)  # Top-left corner
    return None

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    
    # 1. Identify Key Objects
    green_square_coords = find_square(input_grid, 3)
    blue_pixels = find_objects(input_grid, 1)
    magenta_pixels = find_objects(input_grid, 6)

    # 2. Blue Pixel Extension
    if green_square_coords:
      green_square_size = 2
      for blue_pixel in blue_pixels:
        
          row, col = blue_pixel
          
          if row < green_square_coords[0]: # check position relative to the green square
            for i in range(green_square_size * 2):
                if col + 1 + i < output_grid.shape[1]:
                    output_grid[row, col + 1 + i] = 1
          if row > green_square_coords[0]: # check position relative to the green square
            for i in range(green_square_size * 0):
                if col + 1 + i < output_grid.shape[1]:
                    output_grid[row, col + 1 + i] = 1
          if row == green_square_coords[0]:
            pass

    # 3. Magenta Pixel Movement
    if green_square_coords:
        for magenta_pixel in magenta_pixels:
            row, col = magenta_pixel
            if row < green_square_coords[0] + green_square_size and row > green_square_coords[0] - green_square_size : #magenta is above green square
                if row +1 < output_grid.shape[0]:
                    output_grid[row + 1, col] = 6
                    output_grid[row,col] = 0
            if row == green_square_coords[0] + green_square_size and col < green_square_coords[1]:
              output_grid[row,col] = 0
    

    return output_grid
```
