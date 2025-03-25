```python
"""
Transforms the input grid by applying a static color map and implementing a partial vertical reflection within objects colored azure (8).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a predefined color map and a partial vertical reflection rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Static color map derived from training examples
    color_map = {
        0: 0,
        1: 3,
        2: 9,
        3: 1,
        4: 6,
        6: 0,
        7: 2,
        8: 8,
        9: 4,
    }

    # Apply color map
    for r in range(rows):
        for c in range(cols):
            input_color = input_grid[r, c]
            output_grid[r, c] = color_map.get(input_color, input_color)  # Default to original if not in map

    # Apply partial vertical reflection within azure (8) objects
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                # Find the vertical extent of the current 8-colored object
                top = r
                while top > 0 and input_grid[top - 1, c] == 8:
                    top -= 1
                bottom = r
                while bottom < rows - 1 and input_grid[bottom + 1, c] == 8:
                    bottom += 1

                # Find the vertical center of this 8-colored object
                center = (top + bottom) / 2

                # Reflect colors from above the center onto corresponding positions below, if applicable
                if r < center:
                    reflected_row = int(bottom - (r - top))
                    if reflected_row < rows and input_grid[r,c] != 8:
                      output_grid[reflected_row, c] = output_grid[r,c]

    return output_grid.tolist()
```