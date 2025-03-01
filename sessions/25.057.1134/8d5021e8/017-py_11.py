"""
1.  **Identify Input Object:** Find the contiguous region(s) of gray (5) pixels in the input grid. This is the primary "object."
2.  **Determine Output Dimensions:** The output grid is larger than the input grid in all cases. The dimensions appear to be based on padding the input grid, at least doubling its dimensions.
3. **Expand/Replicate Object** Expand the gray pixel region. Also replicate it to adjacent rows and columns to produce repeated 2x2 blocks.
4.  **Pad with Zeros:** Add rows and/or columns of black (0) pixels around all the gray pixels.
"""

import numpy as np

def find_gray_regions(grid):
    """
    Identifies contiguous regions of gray (5) pixels.
    Returns a list of coordinates (row, col) for each gray pixel.
    """
    gray_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 5:
                gray_pixels.append((r, c))
    return gray_pixels

def transform(input_grid):
    # Find gray pixel coordinates
    gray_pixels = find_gray_regions(input_grid)

    if not gray_pixels:
        # Handle cases with no gray pixels (return all zeros)
        output_grid = np.zeros((input_grid.shape[0] * 3, input_grid.shape[1] * 2), dtype=int)
        return output_grid


    # Determine output dimensions (at least double, plus padding)
    output_height = max(input_grid.shape[0] * 3, 9)  #at least triple height or 9
    output_width = max(input_grid.shape[1] *2, 4)

    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate and expand gray regions, ensuring 2x2 blocks
    for r, c in gray_pixels:
      #map input to output
      out_r = r*2 + (output_height - input_grid.shape[0]*2) // 2 #if even number of padding rows
      out_c = c*1+ (output_width - input_grid.shape[1]*1) // 2

      if out_r + 1 < output_height and out_c+1 < output_width:
        output_grid[out_r, out_c] = 5
        output_grid[out_r+1, out_c] = 5
        output_grid[out_r, out_c+1] = 5
        output_grid[out_r+1, out_c+1] = 5

    return output_grid