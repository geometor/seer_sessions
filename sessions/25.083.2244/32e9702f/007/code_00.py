"""
1.  **Background Filling:** Change all pixels with an initial value of 0 (white/background) to 5 (gray).

2.  **Adjacent Pixel Modification:** For any pixel that *was not* originally 0, check if it is adjacent to a pixel that *was* originally 0. If it is, and changing it to 5 would create a one-pixel extension or perimeter of the original non-zero object into the filled background, change the pixel to 5. This means there should not be an isolated 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Helper function to check adjacency to original zero
    def is_adjacent_to_original_zero(r, c, grid):
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                return True
        return False
    
    # Helper function to check for a one-pixel extension
    def is_one_pixel_extension(r,c, original_color, grid):
       
        count = 0
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # count the neighbors that are of the original color
                if grid[nr,nc] == original_color:
                  count += 1
        # check if the pixel has any non-colored neighbors
        #print(f'Pixel Count: {count} for ({r},{c})')
        return count > 0

    # Create a mask for originally zero pixels
    original_zero_mask = (input_grid == 0)

    # 1. Background Filling
    output_grid[original_zero_mask] = 5

    # 2. Adjacent Pixel Modification
    for i in range(rows):
        for j in range(cols):
            # if the value in the input_grid was not zero
            if not original_zero_mask[i, j]:
                # check for a one-pixel extension
                if is_adjacent_to_original_zero(i, j, input_grid) and is_one_pixel_extension(i,j,input_grid[i,j], input_grid):
                    output_grid[i,j] = 5

    return output_grid