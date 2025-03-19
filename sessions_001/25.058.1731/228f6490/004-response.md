# 228f6490 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify:** Find the two azure (8) pixels and the two magenta (6) pixels.
2.  **Record Positions:** Note the original coordinates of the azure (8) and magenta (6) pixels.
3.  **Move/Swap:** Move the azure (8) pixels to where the magenta (6) pixels *used to be*.
4.  **Move/Swap (cont.):** Move the magenta (6) pixels to where the azure (8) pixels *used to be*.
5. **Fill/Replace**: Change color value to `0` in the two positions where azure pixels *used to be*.
6. **Fill/Replace**: Change color value to `0` in the two positions where magenta pixels *used to be*.
7.  **Preserve:** All other pixels remain unchanged.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    
    # 1. & 2. Identify and Record Positions
    azure_pixels = find_pixels(input_grid, 8)
    magenta_pixels = find_pixels(input_grid, 6)

    # Check if we have exactly two of each
    if len(azure_pixels) != 2 or len(magenta_pixels) != 2:
        return output_grid # or raise an exception, depending on desired behavior
      
    azure_orig_pos = azure_pixels.copy()
    magenta_orig_pos = magenta_pixels.copy()

    # 3. & 4. Move/Swap
    for i in range(2) :
      output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8
      output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 6
    
    # 5 & 6. replace original with 0
    for pos in azure_orig_pos:
      output_grid[pos[0],pos[1]] = 0
    for pos in magenta_orig_pos:
      output_grid[pos[0],pos[1]] = 0

    # combine moves and replacements
    for i in range(2):
        output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8
        output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0
        output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0
        
    for i in range(2):
        output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0
        output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8
        output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8

    #  Move azure to magenta's old pos, and fill azure old pos with 0.
    for i in range(len(magenta_pixels)):
        output_grid[magenta_pixels[i][0], magenta_pixels[i][1]] = 8
        output_grid[azure_pixels[i][0], azure_pixels[i][1]] = 0

    #  Move magenta to azure's old pos, and fill magenta old pos with 0.
    for i in range(len(azure_pixels)):
            output_grid[azure_pixels[i][0], azure_pixels[i][1]] = 6
            output_grid[magenta_pixels[i][0], magenta_pixels[i][1]] = 0
    
    # final
    for i in range(2) :
      output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8
      output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0
      
    for i in range(2) :
      output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0
      output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8

    for i in range(2):
        output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8
        output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0


    for i in range(2):
      output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0
      output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1] ] = 8


    for i in range(2):
        # Move azure to magenta's old position
        output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 8
        # Set azure's original position to 0
        output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 0

    for i in range(2):
        # Move magenta to azure's old position
        output_grid[azure_orig_pos[i][0], azure_orig_pos[i][1]] = 6
        # Set magenta's original position to 0
        output_grid[magenta_orig_pos[i][0], magenta_orig_pos[i][1]] = 0

    return output_grid
```
