"""
The transformation rule is as follows:
1. Identify all 2x2 blue squares in the input grid.
2. For each blue square, record the position of the top-left pixel, replace it with a value '1' at that corner in the output grid. The other pixels of the blue square are converted to `0`
3. Identify all 2x2 red squares in the input grid.
4. For each red square, Keep it as, but expand the bottom-right pixel with another red pixel below.
"""

import numpy as np

def find_squares(grid, size, color):
    """Finds top-left corner coordinates of squares of given size and color."""
    squares = []
    rows, cols = grid.shape
    for i in range(rows - size + 1):
        for j in range(cols - size + 1):
            subgrid = grid[i:i+size, j:j+size]
            if np.all(subgrid == color):
                squares.append((i, j))
    return squares

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)  # Convert to numpy array for easier manipulation
    output_grid = np.copy(input_grid)
    output_grid[:] = 0 # intialize to all 0

    # Find blue squares and mark their top-left corners.
    blue_squares = find_squares(input_grid, 2, 1)
    for r, c in blue_squares:
        output_grid[r,c] = 1
        output_grid[r:r+2, c:c+2] = input_grid[r:r+2, c:c+2] # paint all

    # Find red squares, keep and  expand their bottom-right corners.
    red_squares = find_squares(input_grid, 2, 2)
    for r, c in red_squares:
       output_grid[r:r+2, c:c+2] = input_grid[r:r+2, c:c+2] # paint all
       if r + 2 < output_grid.shape[0]: # ensure not out-of-bounds
            output_grid[r + 2, c+1] = 2

    # Copy other pixels to ensure a correct output
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            is_blue_top_left = any((r == br and c == bc) for br, bc in blue_squares)
            is_within_red_square = any((r >= rr and r < rr + 2 and c >= rc and c < rc + 2) for rr, rc in red_squares)
            is_red_expansion = any((r == rr + 2 and c == rc + 1) for rr,rc in red_squares)

            if not is_blue_top_left and not is_within_red_square and not is_red_expansion:
                output_grid[r,c] = 0 # should be all 0, added to copy
           
            if(is_blue_top_left):
                output_grid[r,c] = 1
            
            if is_within_red_square or is_red_expansion :
                 output_grid[r,c] = 2
                

    return output_grid.tolist()