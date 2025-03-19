# d037b0a7 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** the color of the pixel in the top-right corner of the input grid (index [0,2]).
2.  **Propagate** this color to the following pixels:
    *   The pixel in the bottom-right corner (index [2,2]).
    *   The pixel in the center-right (index [1,2]).
    *   The pixel in the bottom center (index [2,1]).
3. **Keep** all other pixels the same.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Get the color of the top-right pixel
    top_right_color = input_grid[0, 2]

    # Propagate the color to the specified pixels
    output_grid[2, 2] = top_right_color
    output_grid[1, 2] = top_right_color
    output_grid[2, 1] = top_right_color
    
    return output_grid
```

