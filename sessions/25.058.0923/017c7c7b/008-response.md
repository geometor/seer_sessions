# 017c7c7b • 008 • example_2 • investigate_coder

---
```python
"""
1. Identify: Locate all blue (1) pixels in the input grid.
2. Extend: add rows to be 50% taller than the original input grid.
3. Substitute: Change the color of all identified blue pixels to red (2).
4. Preserve: Keep all white (0) pixels unchanged.
5. Maintain: Keep the output grid to match the column pattern.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with dimensions 50% taller, filled with white (0)
    input_height, input_width = input_grid.shape
    output_height = input_height + input_height // 2
    output_grid = np.zeros((output_height, input_width), dtype=int)
    
    # Fill the output grid with the pattern, substituting blue with red
    for row in range(output_height):
      for col in range(input_width):
          if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0): # Blue cells in the extended pattern.
              output_grid[row, col] = 2  # change to red (2)
          else:
              output_grid[row,col] = 0

    return output_grid
```
