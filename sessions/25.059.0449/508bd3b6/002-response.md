# 508bd3b6 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Azure Pixels:** Locate all azure (8) pixels in the input grid.
2.  **Green Pixel Insertion:** For each azure pixel:
    *   Begin inserting green (3) pixels diagonally upwards and to the left, starting from the position immediately above and to the left of the azure pixel.
3.  **Termination Condition:** Continue this diagonal insertion of green pixels until:
    *   The edge of the grid is reached.
    *   A red (2) pixel is encountered.
4. **Preservation:** Red pixels are preserved from input to output
"""

import numpy as np

def find_pixels(grid, color):
    # Find coordinates of all pixels of a specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    output_grid = np.copy(input_grid)  # Start with a copy of the input
    azure_pixels = find_pixels(input_grid, 8)

    for y, x in azure_pixels:
        # Green pixel insertion loop
        current_y, current_x = y - 1, x - 1
        while current_y >= 0 and current_x >= 0:  # Check bounds
            if output_grid[current_y, current_x] == 2:  # Check for red pixel
                break
            output_grid[current_y, current_x] = 3  # Insert green pixel
            current_y -= 1
            current_x -= 1

    return output_grid
```
