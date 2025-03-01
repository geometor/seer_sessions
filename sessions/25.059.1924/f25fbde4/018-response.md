# f25fbde4 • 018 • refine_coder

---
```python
"""
1.  **Identify the Yellow Shape:** Locate all yellow (value 4) pixels in the input grid. This constitutes the initial shape.

2.  **Create the Frame:**
    - Create a new grid with the height of original shape + 2, and width of original shape + 1.

3.  **Copy and Frame**:
    - Copy the original shape into the new grid, offset by one row down, and one column to the right.
    - Fill the top row, beginning at column 0, with yellow.
    - Fill the bottom two rows with yellow.

4. **Return Results** Return the expanded grid
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

    # 2. Determine the bounding rectangle (to get dimensions)
    min_row, max_row, min_col, max_col = bounding_rectangle(yellow_coords)
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # 3. Create the base of the new shape (the frame)
    new_height = height + 2
    new_width = width + 1
    new_shape = np.zeros((new_height, new_width), dtype=int)

    # 4. Copy and Frame
    # Copy original shape, offset by one row and one column
    for r in range(height):
        for c in range(width):
            new_shape[r + 1, c + 1] = 4

    # Fill top row with yellow
    for c in range(new_width):
        new_shape[0, c] = 4

    # Fill the last two rows.
    for r in range(new_height-2, new_height):
       for c in range(new_width):
            new_shape[r,c] = 4

    return new_shape.tolist()
```
