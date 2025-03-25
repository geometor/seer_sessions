```python
"""
1.  **Identify Core Rectangle and Border Color:** In the input grid, identify the rectangular block of the same color starting at the top-left corner (the "core rectangle"). The core color is the color of the top-left pixel. Find the "border color," which is the color immediately to the right of or below the core rectangle.
2.  **Create Filled Square:** Create a 9x9 square filled entirely with the core color.
3.  **Add Border:**  Add a border of the border color around the 9x9 square, resulting in a 10x10 output grid. The 10th row and 10th column will be entirely filled with the border color.
"""

import numpy as np

def get_border_color(grid, core_color):
    """Finds the border color adjacent to the core rectangle."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != core_color:
                return grid[r, c]
    return None  # Should not happen in valid cases, but included for completeness

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Core Rectangle and Border Color
    core_color = input_grid[0, 0]
    border_color = get_border_color(input_grid, core_color)

    # 2. Create Filled Square
    output_grid = np.full((9, 9), core_color, dtype=int)

    # 3. Add Border
    output_grid = np.pad(output_grid, pad_width=1, mode='constant', constant_values=border_color)

    return output_grid.tolist()
```