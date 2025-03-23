"""
1. **Reflect:** Reflect the input grid horizontally (across the vertical center line).
2. **Maintain Order:** After reflection, the relative order of colors (based on their first appearance in the input, reading left to right, top to bottom) is maintained.
"""

import numpy as np

def reflect_horizontal(grid):
    """Reflects a grid horizontally."""
    return np.fliplr(grid)

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # 1. Reflect the grid horizontally
    reflected_array = reflect_horizontal(input_array)

    # 2. Maintain Order:  Get color order from original input
    color_order = []
    rows, cols = input_array.shape
    for r in range(rows):
        for c in range(cols):
            color = input_array[r, c]
            color_order.append(color)

    # 3.  Apply the color order to the reflected grid
    output_array = np.zeros_like(reflected_array)
    rows, cols = reflected_array.shape
    color_index = 0
    for r in range(rows):
      for c in range(cols):
        output_array[r,c] = color_order[color_index]
        color_index += 1


    return output_array.tolist()