# a68b268e • 036 • refine_coder

---
```python
"""
1.  **Locate Separator:** Find the horizontal line of blue (1) pixels within the input grid. This line divides the grid into two regions: a "top region" and a "bottom region".

2.  **Identify Corners:**
     - Top Left Corner: Get the top-left pixel of the entire input grid.
     - Top Right Corner: Get the top-right pixel of the entire input grid.
     - Bottom Left Corner: Get the bottom-left pixel from the input grid.
     - Bottom Right Corner. Get the bottom-right pixel from the input grid.

3.  **Construct Output:** Create a 4x4 output grid.
    - Fill rows 0, 1, and 2 with the top-left corner pixel in the first, second, and third columns and the top-right corner pixel in the last column.
    - Fill row 3 with:
        - Columns 0, 1 and 2: the top-left corner pixel
        - Column 3: The bottom-left corner pixel.
"""

import numpy as np

def get_corners(input_grid):
    """Extracts the four corner pixels of the input grid."""
    rows, cols = input_grid.shape
    return {
        'top_left': input_grid[0, 0],
        'top_right': input_grid[0, cols - 1],
        'bottom_left': input_grid[rows - 1, 0],
        'bottom_right': input_grid[rows -1, cols - 1]
    }

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Get the four corners.
    corners = get_corners(input_grid)

    # Initialize the output grid as a 4x4 array.
    output_grid = np.zeros((4, 4), dtype=int)
    
    # Fill rows 0, 1, and 2.
    for row in range(3):
        for col in range(3):
            output_grid[row, col] = corners['top_left']
        output_grid[row, 3] = corners['top_right']

    # Fill row 3.
    for col in range(3):
        output_grid[3,col] = corners['top_left']
    output_grid[3, 3] = corners['bottom_right']

    return output_grid
```
