# 31aa019c • 023 • refine_coder

---
```python
"""
1.  **Initialization:** Start with an output grid filled with white pixels (zeros), the same size as the input grid.
2.  **Find Green Pixels:** Identify the locations of *all* green pixels (value 3) within the input grid.
3.  **Handle Zero Green Pixels:** If no green pixels are found, the output grid remains unchanged (all zeros).
4.  **Create Red Squares:** For *each* green pixel found:
    *   Create a 3x3 square of red pixels (value 2) centered on the green pixel's location.
    *   Place the green pixel (value 3) at the center of the red square, overwriting the red pixel at that location.
5. **Output:** Return the modified grid
"""

import numpy as np

def get_multiple_pixel_locations(grid, color):
  """find all coordinate pairs for the matching color
  """
  coords = np.where(grid == color)
  return list(zip(coords[0],coords[1]))

def transform(input_grid):
    # initialize output_grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)

    # Find all green pixels (value 3)
    green_pixel_locations = get_multiple_pixel_locations(input_grid, 3)

    # Handle zero green pixels case (output remains all zeros)
    if not green_pixel_locations:
        return output_grid

    # Create red squares around each green pixel
    for row, col in green_pixel_locations:
        # Create 3x3 red square
        for i in range(max(0, row - 1), min(output_grid.shape[0], row + 2)):
            for j in range(max(0, col - 1), min(output_grid.shape[1], col + 2)):
                output_grid[i, j] = 2  # Set to red (value 2)

        # Place green pixel in the center
        output_grid[row, col] = 3  # Overwrite with green (value 3)

    return output_grid
```
