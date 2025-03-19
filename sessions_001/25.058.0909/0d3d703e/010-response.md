# 4-0d3d703e • 010 • refine_coder

---
```python
"""
The transformation rule is a simple color substitution. Each digit in the input grid is replaced by a corresponding digit in the output grid according to the following mapping:

1.  Replace all instances of digit '2' (red) with digit '6' (magenta).
2.  Replace all instances of digit '3' (green) with digit '4' (yellow).
3.  Replace all instances of digit '8' (azure) with digit '9' (maroon).

The spatial arrangement of the digits is preserved; only the digit values (colors) are changed.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by applying a color substitution."""
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Define the color mapping
    color_map = {
        2: 6,
        3: 4,
        8: 9,
    }

    # Iterate through the color map and apply the substitutions
    for input_color, output_color in color_map.items():
        output_grid[input_grid == input_color] = output_color

    return output_grid
```

