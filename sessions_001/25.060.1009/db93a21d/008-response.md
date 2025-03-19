# db93a21d • 008 • refine_coder

---
```python
"""
1.  **Identify Maroon Squares:** Locate all maroon (9) squares within the input grid.
2.  **Outline Maroon Squares:** Enclose each maroon square with a one-pixel thick green (3) outline.
3.  **Fill Green outline:** Convert each outlined green area to be a solid green rectangle with the same extent.
4. **Find Green Rectangles:** find *all* green rectangles. If no green, return the input.
5.  **Create Blue Rectangle:**
    - if *one* green rectangle, blue is 2x6 to the right
    - if *two* green rectangles, blue is 6x2 and centered horizontally on right edge of green
    - if more than two, no change (assume)
6. **Output**: return the modified grid.
"""

import numpy as np

def find_squares(grid, color):
    """Finds all squares of a given color, regardless of size."""
    squares = []
    for size in range(1, min(grid.shape) + 1):
        for r in range(grid.shape[0] - size + 1):
            for c in range(grid.shape[1] - size + 1):
                if np.all(grid[r:r+size, c:c+size] == color):
                    squares.append((r, c, size))
    return squares

def outline_square(grid, r, c, size, color):
    """Creates a one-pixel thick outline around a square."""
    # Top
    if r > 0:
        grid[r-1, c:c+size] = color
    # Bottom
    if r + size < grid.shape[0]:
        grid[r+size, c:c+size] = color
    # Left
    if c > 0:
        grid[r:r+size, c-1] = color
    # Right
    if c + size < grid.shape[1]:
        grid[r:r+size, c+size] = color
    return grid

def fill_rectangle(grid, r, c, height, width, color):
    """Fills a rectangular region with a specified color."""
    grid[r:r+height, c:c+width] = color
    return grid

def find_green_rectangle_from_outline(grid, r, c, size):
    """Finds top-left corner of the filled green rect from outlined square."""
    
    outline_r = r - 1
    outline_c = c - 1
    outline_height = size + 2
    outline_width = size + 2
    return (outline_r, outline_c, outline_height, outline_width)
    

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)

    # 1. Identify Maroon Squares
    maroon_squares = find_squares(output_grid, 9)

    # 2. Outline Maroon Squares
    for r, c, size in maroon_squares:
        output_grid = outline_square(output_grid, r, c, size, 3)

    # 3. Fill Green Outlines
    for r, c, size in maroon_squares:
        green_r, green_c, green_h, green_w = find_green_rectangle_from_outline(output_grid,r,c,size)
        output_grid = fill_rectangle(output_grid, green_r, green_c, green_h, green_w, 3)

    # 4. Find Green Rectangles
    green_rectangles = []

    for r, c, size in maroon_squares:
        gr, gc, gh, gw = find_green_rectangle_from_outline(output_grid,r,c,size)
        green_rectangles.append((gr,gc,gh,gw))


    if not green_rectangles:
        return output_grid

    # 5. Create Blue Rectangle
    if len(green_rectangles) == 1:
        r, c, h, w = green_rectangles[0]
        blue_r = r
        blue_c = c + w
        if blue_c < output_grid.shape[1]:
            output_grid = fill_rectangle(output_grid, blue_r, blue_c, 2, 6, 1)
    elif len(green_rectangles) == 2:
        r1, c1, h1, w1 = green_rectangles[0]
        r2, c2, h2, w2 = green_rectangles[1]

        max_right = max(c1 + w1, c2+ w2)
        
        
        avg_top = (r1 + r2) // 2
        blue_r = avg_top
        blue_c = max_right
        if blue_c < output_grid.shape[1]:
           output_grid = fill_rectangle(output_grid,blue_r,blue_c,6,2,1)

    return output_grid
```
