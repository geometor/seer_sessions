# d037b0a7 • 004 • refine_coder

---
```python
"""
1.  **Identify** the color of the pixel at the center-right position `[height // 2, width - 1]` of the input grid.
2.  **Compare** the input grid's center-right pixel's color with its bottom-right pixel's `[height-1, width-1]` color.
3.  **Conditional Change:** If the input colors are the same, then the output grid equals the input grid.
4. **Update**: If different, set the color of the output grid's bottom-right pixel to the color of the input's center-right.
5.  **Iterate**: If the colors were different, set the color of the output grid pixel immediately above the bottom-right to the input's center-right color, and so on, until the center-right output grid pixel is set.
6. **All Other Pixels:** Keep the color values of all other pixels the same as the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Identify the color of the center-right pixel
    center_right_color = input_grid[height // 2, width - 1]
    # Identify the color of the bottom-right pixel
    bottom_right_color = input_grid[height - 1, width - 1]

    # Conditional Change: If different, update bottom-right pixel
    if center_right_color != bottom_right_color:
        for row in range(height -1, height//2 -1, -1):
            output_grid[row, width -1] = center_right_color
    
    return output_grid
```
