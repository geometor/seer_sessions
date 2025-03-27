"""
The transformation rule involves padding the input grid by one layer on each side, using a mirrored reflection of the input grid's edges.

1.  **Input:** Receive a 2D grid of pixels (integers).
2.  **Edge Extraction:** Identify the top, bottom, left, and right edges of the input grid.
3.  **Mirroring:** Create mirrored versions of each edge:
    *   Top and Bottom edges: Flip horizontally.
    *   Left and Right edges: Flip vertically.
4.  **Padding:** Pad the input grid. The padding width will be 1 on each side (top, bottom, left, right). The values used for padding are determined by mirroring the input grid's edges.
5.  **Output:** Return the padded array.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Use numpy's pad function with 'reflect' mode to achieve the mirroring
    output_grid = np.pad(input_grid, pad_width=1, mode='reflect')

    return output_grid.tolist()