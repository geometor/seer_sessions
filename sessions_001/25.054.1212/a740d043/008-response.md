# a740d043 • 008 • example_2 • investigate_coder

---
```python
"""
1. **Identify Distinct Regions:** Scan the input grid to identify contiguous regions of pixels that have a color different from the most frequent color (the background, which is '1' or blue in this case).
2. **Extract Colors:**  Record the color values of these distinct regions. In this example, those are '3' (green) and '2' (red).
3. **Construct Output Grid:** Create a 2x3 output grid.
4. **Populate Output:**  Fill the output grid as follows:
   - First column:  The color of the distinct region encountered *first* when scanning from top-to-bottom and left-to-right (green '3'). Repeat this value for both rows.
   - Second column: Insert the color '0' (white) in both rows.
   - Third column: The color of the distinct region encountered *second* (red '2'). Repeat this value for both rows.
"""

import numpy as np
from collections import Counter

def find_distinct_regions(grid):
    # Find the most frequent color (background)
    colors = Counter(grid.flatten())
    background_color = colors.most_common(1)[0][0]

    distinct_colors = []
    for color in colors:
        if color != background_color:
            distinct_colors.append(color)
    
    return distinct_colors, background_color

def transform(input_grid):
    # Find distinct regions and their colors
    distinct_colors, _ = find_distinct_regions(input_grid)
    
    # Sort the distinct colors based on their first appearance top->bottom, left->right
    color_positions = {}
    for row_idx, row in enumerate(input_grid):
        for col_idx, pixel in enumerate(row):
            if pixel in distinct_colors and pixel not in color_positions:
                color_positions[pixel] = (row_idx, col_idx)

    sorted_colors = sorted(distinct_colors, key=lambda color: color_positions.get(color, (float('inf'), float('inf'))))

    # Create a 2x3 output grid
    output_grid = np.zeros((2, 3), dtype=int)

    # Populate the output grid
    if len(sorted_colors) > 0:
      output_grid[:, 0] = sorted_colors[0]  # First distinct color
    output_grid[:, 1] = 0          # Insert '0' (white)
    if len(sorted_colors) > 1:
      output_grid[:, 2] = sorted_colors[1]  # Second distinct color

    return output_grid
```
