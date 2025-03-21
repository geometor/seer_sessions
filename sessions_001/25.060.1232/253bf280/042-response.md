# 253bf280 • 042 • refine_coder

---
```python
"""
1.  **Locate Azure Pixels:** Identify all pixels in the input grid that are colored azure (8).
2.  **Count Azure Pixels:** Determine the number of azure pixels found.
3.  **Determine Green Line Column:** The green line will be drawn in the same column as the azure pixels.
4.  **Determine Green line length and position:** The green line will have a height equal to the number of azure pixels, bound by the grid size.
5.  **Draw Green Line:** Create a vertical line of green (3) pixels in the output grid. The line's length is equal to the number of azure pixels found in the input. The line is in the same column as the azure pixels, and it should stay within the bounds of the output grid.
6. **No Azure Pixels:** If no azure pixels are found, return a copy of the input grid.
"""

import numpy as np

def get_azure_pixels(grid):
    # Find coordinates of azure (8) pixels
    azure_coords = np.where(grid == 8)
    return list(zip(azure_coords[0], azure_coords[1]))

def transform(input_grid):
    """Transforms the input grid by drawing a vertical green line based on azure pixels."""

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the azure pixels
    azure_pixels = get_azure_pixels(input_grid)

    # If no azure pixels are found, return a copy of the input
    if not azure_pixels:
        return output_grid

    # Determine the column for the green line
    column = azure_pixels[0][1]

    # Determine the number (count) of azure pixels for the green line height
    num_azure_pixels = len(azure_pixels)

    # Determine the starting row.  The first azure pixel could be anywhere.
    start_row = azure_pixels[0][0]

    # Draw the green line (3), with height equal to count of azure pixels
    for i in range(num_azure_pixels):
        row = start_row + i
        if 0 <= row < output_grid.shape[0]:  # stay within bounds
            output_grid[row, column] = 3

    return output_grid
```
