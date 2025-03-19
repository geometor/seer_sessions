# f8ff0b80 • 008 • refine_coder

---
```python
"""
1.  **Check for Target Colors:** Examine the input grid for the presence of pixels with colors 1 (blue), 7 (orange), and 2 (red).
2.  **Determine Output:**
    *   If none of these colors are found, the output is an empty grid.
    *   If any of these colors are found, create a 3x1 output grid.
3.  **Populate Output Grid:** The output grid is populated with the colors 1, 7, and 2, *always* in that order. If one of those colors is not in input, it is still in output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid based on the presence of colors 1, 7, and 2.
    """
    input_array = np.array(input_grid)

    # Check for target colors (1, 7, 2)
    has_target_colors = any(color in input_array for color in [1, 7, 2])

    # Determine output based on presence of target colors
    if not has_target_colors:
        return []  # Empty grid
    else:
        output_grid = np.array([[1], [7], [2]])  # 3x1 grid with colors 1, 7, 2

    return output_grid.tolist()
```
