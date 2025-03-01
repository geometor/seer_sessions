# bbc9ae5d • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify the initial contiguous sequence of gray (5) pixels at the beginning of the input row.
2. Determine the output grid dimensions: The width matches the input width, and the height is determined by the number of gray pixels.
3. Copy the input to the first row of the output grid.
4. Expand the gray region: For each subsequent row, increase the number of gray pixels by one, starting from the initial gray region length. This forms a growing triangle.
5. Fill the remaining space: Fill the remaining cells of the output grid with white (0) pixels.
"""

import numpy as np

def get_gray_region_length(input_grid):
    """
    Helper Function: count the length of the initial continuous gray region in the input grid.
    """
    count = 0
    for pixel in input_grid:
        if pixel == 5:
            count += 1
        else:
            break  # Stop when a non-gray pixel is encountered
    return count

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    gray_length = get_gray_region_length(input_grid)
    output_height = gray_length + input_grid.size - gray_length #this calculates correctly, gray and white regions sizes add to total length
    output_width = input_grid.shape[0]

    # initialize output_grid with the calculated dimensions, filled with input pixels
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    output_grid[0,:] = input_grid

    # Expand the gray region downwards and rightwards.
    
    for row in range(1,output_height):       
        gray_count = min(gray_length + row, output_width)
        for col in range(gray_count):
            output_grid[row, col] = 5

    return output_grid
```
