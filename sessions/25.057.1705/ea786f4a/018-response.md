# ea786f4a • 018 • refine_coder

---
```python
"""
1.  **Identify the Trigger:** Find a single-pixel object in the input grid. If one is not found, consider the entire input grid as a single object and consider its top-left pixel as the "trigger" location.
2.  **Center Color:** Note the color of the trigger pixel.
3.  **Cross Creation:** Create a white cross in the output grid. The center of this cross is positioned at the location of the trigger pixel (or the top-left pixel if no single-pixel object was found).
4. **Center Pixel**: Set the color of the center pixel of the cross to the color recorded in step 2.
5.  **Cross Extent:** The arms of the cross extend from the center until the edges of the grid.
"""

import numpy as np

def find_trigger_pixel(grid):
    # Find single-pixel objects.
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is isolated (not surrounded by same color).
            is_isolated = True
            color = grid[r, c]

            # Check neighbors (up, down, left, right)
            if r > 0 and grid[r-1, c] == color:
                is_isolated = False
            if r < rows - 1 and grid[r+1, c] == color:
                is_isolated = False
            if c > 0 and grid[r, c-1] == color:
                is_isolated = False
            if c < cols - 1 and grid[r, c+1] == color:
                is_isolated = False

            if is_isolated:
                return (r, c)

    # If no isolated pixel found, return top-left.
    return (0, 0)

def transform(input_grid):
    # Initialize output_grid as all white.
    output_grid = np.zeros_like(input_grid)

    # Find the trigger pixel and its color.
    trigger_row, trigger_col = find_trigger_pixel(input_grid)
    trigger_color = input_grid[trigger_row, trigger_col]

    rows, cols = output_grid.shape
    
    # Create the white cross.
    for r in range(rows):
        output_grid[r, trigger_col] = 0  # White
    for c in range(cols):
        output_grid[trigger_row, c] = 0  # White

    # Set the center color.
    output_grid[trigger_row, trigger_col] = trigger_color

    return output_grid
```
