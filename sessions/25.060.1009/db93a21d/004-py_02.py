"""
1.  **Identify Maroon Squares:** Locate all 2x2 maroon (9) squares in the input grid. In this case we have two of such squares.

2.  **Outline Maroon Squares:** For each identified maroon square, create a green (3) outline. The green outline replaces the white(0) pixels that are directly adjacent (up, down, left and right, not diagonally) to the maroon square, and maintains the original dimensions, hence the outline will be inside the grid and will be one pixel thick.

3.  **Create Blue Rectangle:** Create a 2x6 blue (1) rectangle in the center-right portion of the grid. This blue block should start directly adjacent/to the right of the outline of the lower maroon block, spanning vertically six cells down.

4. **Extend Green outline:** expand the green outlines created in step 2, so it become a filled rectangle of the same dimensions.

5.  **Output:** The final output grid combines all these transformations.
"""

import numpy as np

def find_squares(grid, color, size):
    squares = []
    for r in range(grid.shape[0] - size + 1):
        for c in range(grid.shape[1] - size + 1):
            if np.all(grid[r:r+size, c:c+size] == color):
                squares.append((r, c))
    return squares

def outline_square(grid, r, c, size, color):
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
   grid[r:r+height, c:c+width] = color
   return grid
    

def transform(input_grid):
    output_grid = np.copy(input_grid)

    # 1. Identify Maroon Squares
    maroon_squares = find_squares(output_grid, 9, 2)

    # 2. Outline Maroon Squares and then extend to filled rectangle.
    for r, c in maroon_squares:
      output_grid = outline_square(output_grid,r,c,2,3)
    for r,c in maroon_squares:
        # find green outline coordinates
        green_squares = find_squares(output_grid, 3, 2)
        for gr,gc in green_squares:
            if (abs(gr-r) <= 2) and (abs(gc -c) <=2):
               output_grid = fill_rectangle(output_grid,gr,gc,4,4,3)



    # 3. Create Blue Rectangle
    #find bottom left square
    maroon_squares.sort()
    bl_r, bl_c = maroon_squares[0] if maroon_squares else (0,0)

    blue_r = bl_r
    blue_c = bl_c + 2 + 2 #original block + outline

    if blue_c < output_grid.shape[1]:
        output_grid = fill_rectangle(output_grid, blue_r, blue_c, 6, 2, 1)
    


    return output_grid