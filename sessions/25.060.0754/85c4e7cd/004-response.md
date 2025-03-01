# 85c4e7cd • 004 • example_1 • investigate_coder

---
```python
"""
The transformation inverts the color layers of the nested squares. The outermost color in the input becomes the outermost color in the output, and so on. The color mapping is as follows:

- Yellow (4) -> Azure (8)
- Red (2) -> Grey (5)
- Blue (1) -> Green (3)
- Green (3) -> Blue (1)
- Grey (5) -> Red (2)
- Azure (8) -> Yellow (4)
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # color mapping dictionary
    color_map = {
        4: 8,
        2: 5,
        1: 3,
        3: 1,
        5: 2,
        8: 4
    }

    # change output pixels based on the color map
    for i in range(rows):
        for j in range(cols):
            input_color = input_grid[i, j]
            output_grid[i, j] = color_map.get(input_color, input_color) # Use .get() to handle potential missing keys

    return output_grid
```
