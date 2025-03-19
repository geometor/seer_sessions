# 1e0a9b12 • 008 • refine_coder

---
```python
"""
1.  **Extract Non-Zero Pixels:** Identify all pixels in the input grid that have a non-zero value. Store these pixels, preserving their color and their original order of appearance, reading left-to-right, top-to-bottom.
2.  **Reorder Non-Zero Pixels:** Sort these pixels based on their original row values (ascending).
3. **Place in Output:** Place these ordered non-zero pixel colors into the last row of the output grid. Start from the leftmost column and proceed rightward.
4.  **Fill Remaining:** Fill any remaining empty cells in the output grid with 0 (white).
"""

import numpy as np

def get_nonzero_pixels(grid):
    rows, cols = np.nonzero(grid)
    return [(r, c, grid[r, c]) for r, c in zip(rows, cols)]

def transform(input_grid):
    # Initialize output grid with zeros, same shape/type as input.
    output_grid = np.zeros_like(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]
    
    # Extract non-zero pixels (color and position).
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # Sort non-zero pixels by their original row (ascending).
    nonzero_pixels.sort(key=lambda x: x[0])

    # Extract the color values from the sorted pixels.
    nonzero_values = [pixel[2] for pixel in nonzero_pixels]

    # Place the non-zero values in the bottom row.
    for i, value in enumerate(nonzero_values):
        if i < cols:  # Prevent index out of bounds if more values than cols
            output_grid[rows - 1, i] = value

    return output_grid
```
