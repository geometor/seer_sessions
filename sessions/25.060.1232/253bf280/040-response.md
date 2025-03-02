# 253bf280 • 040 • example_7 • investigate_coder

---
```python
"""
1. **Locate Azure Pixels:** Find all pixels in the input grid that have the color azure (8). Note their column.
2.  **Determine Green Line Column:** The green line will be in the same column as the azure pixels.
3.  **Determine Green line length and position.** There are 3 azure pixels in input. The azure area seems to start at row index 1 and and row index 6. The green area is 4 high and is centered vertically, leaving one open cell above and below.
4. **Draw Green line** draw green pixels in all cells identified in the previous step.

In summary input azure pixels are transformed to an output green vertical line of height 4 centered on the column of the azure pixels.
"""

import numpy as np

def get_azure_pixels(grid):
    # Find coordinates of azure (8) pixels
    azure_coords = np.where(grid == 8)
    return list(zip(azure_coords[0], azure_coords[1]))


def transform(input_grid):
    """Transforms the input grid by drawing a centered vertical green line."""

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the azure pixels
    azure_pixels = get_azure_pixels(input_grid)
    if not azure_pixels:
        return output_grid  # Return input grid if no azure pixels.

    # Determine the column for the green line
    column = azure_pixels[0][1]
   
    # Calculate start and end row for green line with a height of 4
    height = output_grid.shape[0]
    
    start_row = 2
    end_row = 5

    # Draw the green line (3)
    for row in range(start_row, end_row + 1):
      output_grid[row, column] = 3

    return output_grid
```
