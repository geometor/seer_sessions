```python
"""
1. Scan the input grid from left to right, top to bottom.
2. Identify all distinct non-zero colors.
3. Record the colors in the order in which their *first instance* is encountered.
4. Create an output grid.
5. for each color, create a new row in the output and place the color value. The number of rows is determined by the number of unique colors identified.
6. Return the new output grid, containing a one color of each type stacked in order
"""

import numpy as np

def get_distinct_colors(input_grid):
    """
    Finds distinct non-zero colors in the input grid, preserving the order of first appearance.
    """
    distinct_colors = []
    seen_colors = set()
    for row in input_grid:
        for cell in row:
            if cell != 0 and cell not in seen_colors:
                distinct_colors.append(cell)
                seen_colors.add(cell)
    return distinct_colors

def transform(input_grid):
    # Find distinct colors in order of appearance
    distinct_colors = get_distinct_colors(input_grid)

    # Create output grid
    num_distinct_colors = len(distinct_colors)
    if num_distinct_colors == 0:
        output_grid = np.array([[]])  # Return an empty array if input grid is empty or no colors
    else:
      output_grid = np.array(distinct_colors).reshape(-1,1)

    if output_grid.size > 0:
       output_grid = np.tile(output_grid, (1,len(set(output_grid.flatten()))))
       output_grid = [r[:len(set(distinct_colors))] for r in output_grid]

    return np.array(output_grid)
```