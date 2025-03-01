"""
1.  **Identify the yellow shape:** Locate all pixels with the value '4' (yellow) in the input grid. This defines the initial shape.

2.  **Determine the bounding rectangle:** Find the minimum and maximum row and column indices occupied by the yellow pixels. This effectively creates a bounding box around the initial shape.

3.  **Create the base of the new shape:**
    - create new shape based on height and width of original.
    - new shape row count = original shape height + 1.
    - new shape column count = original shape width +1.

4. **Fill and Expand:**
    -   copy original shape into top left of new shape
    -   replicate the new shape's top row, one column to the left, and append to the left of the shape
    - replicate the new shapes's first two rows and append below
    -   result is an output grid with this larger rectangle of '4's.
"""

import numpy as np

def find_shape(grid, color):
    """Finds the coordinates of a shape of a specific color in the grid."""
    coords = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                coords.append((r_idx, c_idx))
    return coords

def bounding_rectangle(coords):
    """Calculates the bounding rectangle of a set of coordinates."""
    if not coords:
        return 0,0,0,0
    min_row = min(c[0] for c in coords)
    max_row = max(c[0] for c in coords)
    min_col = min(c[1] for c in coords)
    max_col = max(c[1] for c in coords)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Identify the yellow shape
    yellow_coords = find_shape(input_grid, 4)

    # 2. Determine the bounding rectangle
    min_row, max_row, min_col, max_col = bounding_rectangle(yellow_coords)
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # 3. Create the base of the new shape
    new_height = height + 2
    new_width = width + 1
    new_shape = np.zeros((new_height, new_width), dtype=int)

    # 4. Fill and expand
    # Copy original shape into top left
    for r in range(height):
      for c in range(width):
        new_shape[r,c+1] = 4
    # replicate top row one col left
    for c in range(width):
      new_shape[0,0] = 4

    # replicate first two rows below
    for r in range(2):
        for c in range(new_width):
          new_shape[new_height-2+r,c]=new_shape[r,c]

    # Pad to fit original image and shift to accomodate expansion
    output_grid = np.zeros((max(input_grid.shape[0], new_shape.shape[0]), max(input_grid.shape[1],new_shape.shape[1])),dtype=int)
    row_shift = 0
    col_shift = 0

    output_grid[row_shift:row_shift + new_shape.shape[0], col_shift:col_shift+new_shape.shape[1]] = new_shape
    output_grid = output_grid[:8,:6]

    return output_grid.tolist()