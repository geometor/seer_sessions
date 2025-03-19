"""
1.  **Identify Maroon Squares:** Find all maroon (9) squares in the input grid. Note their size (which can vary).
2.  **Outline Maroon Squares:** Create a green (3) outline, one pixel thick, around each identified maroon square. The outline should be directly adjacent to the maroon square on all four sides (top, bottom, left, right).
3. **Fill Green outline:** Convert each outlined green area to be a solid green rectangle with the same extent.
4.  **Find Bottom-Most Green Rectangle:** Determine the green rectangle that is positioned lowest in the grid. If there are multiple at the same vertical level, no operation. If no green rectangles are found - no operation.
5.  **Create Blue Rectangle:** Create a 2x6 blue (1) rectangle. Position the top-left corner of this rectangle directly to the right of the *bottom-most* green rectangle.
6. **Output**: output the modified grid.
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

    # 4. Find Bottom-Most Green Rectangle
    green_rectangles = []

    for r, c, size in maroon_squares:
        gr, gc, gh, gw = find_green_rectangle_from_outline(output_grid,r,c,size)
        green_rectangles.append((gr,gc,gh,gw))


    if not green_rectangles:
        return output_grid

    bottom_most_y = -1
    bottom_most_rect = None
    
    for r, c, h, w in green_rectangles:
        bottom_y = r + h
        if bottom_y > bottom_most_y:
            bottom_most_y = bottom_y
            bottom_most_rect = (r, c, h, w)
        elif bottom_y == bottom_most_y: # multiple at same level
             return output_grid

    if bottom_most_rect is None: return output_grid

    # 5. Create Blue Rectangle
    blue_r = bottom_most_rect[0]
    blue_c = bottom_most_rect[1] + bottom_most_rect[3]

    if blue_c < output_grid.shape[1]:  # Check for out-of-bounds
       output_grid = fill_rectangle(output_grid, blue_r, blue_c, 6, 2, 1)

    return output_grid