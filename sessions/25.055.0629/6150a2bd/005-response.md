# 6150a2bd • 005 • refine_coder

---
```python
"""
1.  **Identify the Object:** Locate the single 2x2 square object composed of green (color code 3) pixels within the input grid.
2.  **Recolor the Object:** Change the color of all pixels within the identified 2x2 square object to blue (color code 1).
3.  **Preserve the Background:** Keep all other pixels (the white background, color code 0) unchanged.
4.  **Output:** The output grid is the same size as the input, with the identified square now colored blue, and all other pixels remaining white.
"""

import numpy as np

def find_2x2_square(grid, color):
    # Find a 2x2 square of the specified color.
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            if (grid[r, c] == color and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                return [(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)]
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the 2x2 green square
    green_square_coords = find_2x2_square(output_grid, 3)

    # If a green square is found, recolor it to blue
    if green_square_coords:
        for r, c in green_square_coords:
            output_grid[r, c] = 1

    return output_grid
```
