# ff28f65a • 018 • refine_coder

---
```python
"""
1.  **Identify Red Regions:** Locate all 2x2 contiguous blocks of red (value 2) pixels within the input grid.
2.  **Determine Output Grid Mapping:**  Divide the input grid into nine regions, corresponding to the 3x3 output grid. The regions are determined by dividing the input grid's height and width by 3.
3.  **Abstract Representation:** Create a 3x3 output grid initialized with white (0).
4.  **Presence Check:** For each cell in the 3x3 output grid:
    -   Determine the corresponding region in the input grid.
    -   Check if *any* 2x2 red square exists *anywhere* within that region.
    -   If a red square is found within the region, set the output cell to blue (1). Otherwise, leave it as white (0).

"""

import numpy as np

def find_squares(grid, size, color):
    """Finds all contiguous blocks of a specified size and color."""
    squares = []
    for i in range(grid.shape[0] - size + 1):
        for j in range(grid.shape[1] - size + 1):
            if np.all(grid[i:i+size, j:j+size] == color):
                squares.append((i, j))
    return squares

def transform(input_grid):
    """Transforms the input grid according to the presence of 2x2 red squares."""
    output_grid = np.zeros((3, 3), dtype=int)
    red_squares = find_squares(input_grid, 2, 2)
    
    height, width = input_grid.shape
    row_step = height / 3.0
    col_step = width / 3.0

    for i in range(3):
        for j in range(3):
            # Define the boundaries of the current region
            row_start = int(i * row_step)
            row_end = int((i + 1) * row_step)
            col_start = int(j * col_step)
            col_end = int((j + 1) * col_step)
            
            # Check for any red squares within this region
            for r_sq in red_squares:
                if row_start <= r_sq[0] < row_end and col_start <= r_sq[1] < col_end:
                    output_grid[i, j] = 1
                    break  # Once a square is found in the region, move to the next output cell
                # also check if the square ends inside the region
                if row_start <= r_sq[0]+1 < row_end and col_start <= r_sq[1]+1 < col_end:
                    output_grid[i, j] = 1
                    break

    return output_grid
```
