"""
1.  **Identify the Non-Zero Pixel:** Find the single pixel in the input grid that has a non-zero value. Note its color and original (row, column) position.
2.  **Diagonal Replication:** Replicate this pixel diagonally in both directions (up-left, up-right, down-left, down-right).
3.  **Modulo Operation/Edge Wrapping**: use the modulo operator with respect to the length/width in the direction of expansion. The new coordinates for a copy will by ( (row + i) % height, (col + i) % width) and ((row - i) % height, (col - i) % width) where height and width are grid dimensions and row/col are the original row/column location of the non zero pixel. i is the index of the copy.
4.  **Output Grid:** Create an output grid of the same dimensions as the input. Place copies of the identified non-zero pixel value into the output grid according to the diagonal pattern and the edge wrapping rule. All other pixels in the output grid remain 0.
"""

import numpy as np

def find_non_zero_pixel(grid):
    """Finds the (row, col) of the single non-zero pixel."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return (r, c, grid[r,c])
    return None  # Should not happen in valid inputs, based on problem definition

def transform(input_grid):
    """Transforms the input grid by replicating the non-zero pixel diagonally."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero pixel
    non_zero_pixel_info = find_non_zero_pixel(input_grid)
    if non_zero_pixel_info is None:
        return output_grid #return blank if no non-zero pixel
    
    orig_row, orig_col, color = non_zero_pixel_info

    # Replicate diagonally with wrapping
    for i in range(max(rows, cols)):
        #Up-Right and Down-Left
        output_grid[(orig_row + i) % rows, (orig_col + i) % cols] = color
        output_grid[(orig_row - i) % rows, (orig_col - i) % cols] = color


    return output_grid.tolist()