# AboveBelow7 • 004 • refine_coder

---
```python
"""
1.  **Identify Objects:**
    *   Find a rectangle object (contiguous block of pixels of the same color). Record its color, top-left, and bottom-right coordinates.
    *   Find a U-shaped object (contiguous block of pixels forming a 'U' shape, opening upwards). Record its color, and bounding box. The color may vary.
2.  **Handle Missing Objects:**
    *   If either the rectangle or the U-shape is not found, return the input grid unchanged.
3. **Determine new position:**
    * Find the top most row of the rectangle.
    * Find the top most row of the U-shape.
4.  **Swap Positions:**
    *   Clear the original positions of both objects in the output grid.
    *   Redraw the rectangle at the original vertical position of the U-shape.
    *   Redraw the U-shape at the original vertical position of the rectangle.
5.  **Preserve Other Pixels:**
    * Ensure all other pixels in the grid remain unchanged.
"""

import numpy as np

def find_rectangle(grid):
    """Finds a rectangle in the grid and returns its properties."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None  # No rectangle found

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    color = grid[min_row, min_col]

    # Check if it's a contiguous rectangle
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if grid[r, c] != color:
                return None  # Not a contiguous rectangle

    return {
        "name": "rectangle_1",
        "color": color,
        "shape": "rectangle",
        "top_left": (min_row, min_col),
        "bottom_right": (max_row, max_col),
        "coords": [(r, c) for r in range(min_row, max_row+1) for c in range(min_col, max_col + 1)]
    }

def find_u_shape(grid):
    """Finds a U-shape in the grid and returns its properties."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    
    for color in np.unique(grid[rows, cols]): # check each found color
        coords = []
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if grid[r,c] == color:
                    coords.append((r,c))

        # Check for U-shape (opening upwards)
        if len(coords) > 3: # Needs at least 4 for a u-shape
            # find left, right, bottom
            u_rows, u_cols = zip(*coords)  # Unzip coordinates

            left_col = min(u_cols)
            right_col = max(u_cols)
            bottom_row = max(u_rows)
            
            # basic validation for u-shape
            left_count = sum(1 for r, c in coords if c == left_col)
            right_count = sum(1 for r, c in coords if c == right_col)
            bottom_count = sum(1 for r, c in coords if r == bottom_row)

            if left_count >= 2 and right_count >= 2 and bottom_count >= 2:
               return{
                    "name": "u_shape_1",
                    "color": color,
                    "shape": "u-shape",
                    "top_left": (min_row, min_col),
                    "bottom_right": (max_row, max_col),
                    "coords": coords
                }
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Identify Objects
    rectangle = find_rectangle(input_grid)
    u_shape = find_u_shape(input_grid)
    
    # Handle Missing Objects
    if rectangle is None or u_shape is None:
        return output_grid
    
    # Clear original positions
    for r, c in rectangle["coords"]:
        output_grid[r, c] = 0
    for r, c in u_shape["coords"]:
        output_grid[r, c] = 0
    
    # Determine new position
    rect_top_row = rectangle["top_left"][0]
    u_shape_top_row = u_shape["top_left"][0]
    
    # Swap positions:  rectangle
    row_shift = u_shape_top_row - rect_top_row
    for r, c in rectangle["coords"]:
        new_r = r + row_shift
        if 0 <= new_r < output_grid.shape[0]:  # boundary check
            output_grid[new_r, c] = rectangle["color"]
    
    # Swap positions: U-Shape
    row_shift = rect_top_row - u_shape_top_row
    for r, c in u_shape["coords"]:
        new_r = r + row_shift
        if 0 <= new_r < output_grid.shape[0]:  # boundary check
            output_grid[new_r, c] = u_shape["color"]

    return output_grid
```
