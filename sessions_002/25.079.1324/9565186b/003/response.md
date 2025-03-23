```python
"""
1.  **Find Azure Pixels:** Iterate through the input grid and create a list of the coordinates of all pixels that are color 8 (azure).
2.  **Process Rows:** For each azure pixel coordinate, iterate through its row in the input grid. If a pixel in that row is not color 2 (red), change the pixel in the *output* grid at the corresponding location to color 5 (grey).
3.  **Process Columns:** For each azure pixel coordinate, iterate through its column in the input grid. If a pixel in that column is not color 2 (red), change the pixel in the *output* grid at the corresponding location to color 5 (grey).
4. **Output:** Return the modified output grid.
"""

import numpy as np

def find_azure_pixels(grid):
    """
    Finds the coordinates of all azure (8) pixels in the grid.
    """
    rows, cols = grid.shape
    azure_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 8:
                azure_pixels.append((r, c))
    return azure_pixels

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all azure pixels
    azure_pixels = find_azure_pixels(input_grid)

    # Process Rows
    for r, c in azure_pixels:
        for i in range(cols):
            if input_grid[r, i] != 2:  # If not red
                output_grid[r, i] = 5  # Change to grey

    # Process Columns
    for r, c in azure_pixels:
        for j in range(rows):
            if input_grid[j, c] != 2:  # If not red
                output_grid[j, c] = 5  # Change to grey

    return output_grid
```