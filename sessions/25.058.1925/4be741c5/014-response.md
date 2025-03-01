# 4be741c5 • 014 • refine_coder

---
```python
"""
1.  **Identify Unique Colors:** Find all unique colors present in the entire input grid, regardless of row or column.
2.  **Preserve Order:** Maintain the order in which these unique colors first appear in the input grid (considering the grid read from left-to-right and top-to-bottom).
3.  **Construct Output Grid:** Create a new grid with dimensions 1 x N, where N is the number of unique colors found in step 1.
4.  **Populate Output Grid:** Populate the output grid with the ordered, unique colors identified in steps 1 and 2.
"""

import numpy as np

def get_unique_colors_preserved_order(grid):
    """
    Extracts unique colors from a 2D grid, preserving their original order of appearance.
    """
    unique_colors = []
    for row in grid:
        for color in row:
            if color not in unique_colors:
                unique_colors.append(color)
    return unique_colors

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Identify unique colors, preserving order
    unique_colors = get_unique_colors_preserved_order(input_grid)

    # Construct output grid (1 x N)
    output_grid = np.array(unique_colors).reshape(1, -1)

    return output_grid
```
