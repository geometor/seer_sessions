```python
"""
Iterates through each pixel of the input grid. If a pixel's color is one of the target colors,
it checks its eight neighbors. If any neighbor has a lower color value, the lower-valued neighbor in the output grid becomes azure (8).
Pixels of color white (0) or azure (8) remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on color adjacency rules.
    
    If a region that is not color 'white' is adjacent to a pixel of lower value of another non-white region, that lower value pixel will change color to 8(azure).
    Adjacency includes diagonals.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            current_color = input_grid[r, c]

            # Skip if the current pixel is white or azure
            if current_color == 0 or current_color == 8:
                continue

            # Check all eight neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue  # Skip the pixel itself

                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_color = input_grid[nr, nc]

                        # Apply the color change rule: current pixel is non-white/azure, and a non-white/azure neighbor has a *lower* value
                        if neighbor_color != 0 and neighbor_color != 8 and neighbor_color < current_color :
                            output_grid[nr, nc] = 8

    return output_grid
```