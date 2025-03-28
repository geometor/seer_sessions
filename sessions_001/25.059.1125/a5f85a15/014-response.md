# a5f85a15 • 014 • example_2 • investigate_coder

---
```python
"""
Change maroon (9) pixels to yellow (4) if and only if they are diagonally adjacent to other maroon pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing maroon (9) pixels to yellow (4)
    if they are diagonally adjacent to other maroon pixels.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    def is_diagonally_adjacent_to_maroon(row, col, grid):
        """
        Checks if a pixel at (row, col) is diagonally adjacent to another maroon pixel.
        """
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # Skip the cell itself
                new_row, new_col = row + i, col + j
                if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row, new_col] == 9:
                    return True
        return False

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is maroon
            if input_grid[row, col] == 9:
                # Check for diagonal adjacency to other maroon pixels
                if is_diagonally_adjacent_to_maroon(row, col, input_grid):
                    # Change color to yellow
                    output_grid[row, col] = 4

    return output_grid
```
