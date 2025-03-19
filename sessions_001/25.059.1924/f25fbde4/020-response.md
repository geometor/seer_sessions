# f25fbde4 • 020 • refine_coder

---
```python
"""
1.  **Identify the Yellow Shape:** Locate all yellow (value 4) pixels in the input grid. This forms the original shape.

2.  **Determine Dimensions:** Calculate the height and width of the original shape.

3.  **Create New Grid:** Create a new grid with height = original height + 2, and width = original width + 1.

4.  **Copy Shape:** Copy the original yellow shape into the new grid, with an offset of one row down and one column to the right.

5.  **Add Frame - Top Row:** Fill the top row of the new grid with yellow, starting at column 0 (one column to the left of original shape).

6. **Add Frame - Bottom Rows**: Fill the bottom two rows with yellow.

7.  **Return:** Return the modified grid.
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

    # 5. Fill top row with yellow, starting at column 0
    for c in range(new_width):
        new_shape[0, c] = 4

    # 6. Fill the last two rows.
    for r in range(new_height-2, new_height):
       for c in range(new_width):
            new_shape[r,c] = 4

    return new_shape.tolist()
```
