```python
"""
The transformation rule is a simple color substitution. Each color in the input grid is replaced by a corresponding color in the output grid, according to a fixed mapping. The mapping is as follows:

1.  Replace all occurrences of color 3 (green) with color 4 (yellow).
2.  Replace all occurrences of color 1 (blue) with color 5 (gray).
3.  Replace all occurrences of color 2 (red) with color 6 (magenta).
4.  Replace all occurrences of color 8 (azure) with color 9 (maroon).
5.  Replace all occurrences of color 5 (gray) with color 1 (blue).
6.  Replace all occurrences of color 6 (magenta) with color 2 (red).
7.  Replace all occurrences of color 9 (maroon) with color 8 (azure).
8.  Replace all occurrences of color 4 (yellow) with color 3 (green).

This mapping is applied uniformly to every pixel in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by applying a fixed color mapping.
    """
    # Create a copy of the input grid to serve as the output grid.  We modify this copy.
    output_grid = np.copy(input_grid)

    # Define the color mapping as a dictionary.
    color_map = {
        3: 4,
        1: 5,
        2: 6,
        8: 9,
        5: 1,
        6: 2,
        9: 8,
        4: 3
    }

    # Iterate through the color map and apply the substitutions.
    for input_color, output_color in color_map.items():
        output_grid[input_grid == input_color] = output_color
    
    return output_grid
```
