"""
1.  **Identify Seed Pixels:** Locate all pixels in the input grid that have a non-zero value. These are the "seed" pixels.
2.  **For Each Seed Pixel:**
    *   Create a rectangular region filled with the seed pixel's color.
    *   The rectangle's top-left corner will alternate position, depending on parity:
        *   If the seed pixel is the first seed pixel encountered scanning the grid in row-major order, it's top-left corner is that seed pixel, and the lower-right corner will be the bottom right-hand corner of the grid.
        *   If the seed pixel is the second seed pixel, it's top-left corner will be top-left corner of the grid, and bottom right corner is the location of that seed pixel.
3. **Combine the regions**
4.  **Output:** Return the modified grid.
"""

import numpy as np

def find_seed_pixels(grid):
    """Finds non-zero pixels (seed pixels) in the grid."""
    seed_pixels = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                seed_pixels.append((r, c, value))
    return seed_pixels

def transform(input_grid):
    """Transforms the input grid according to the flooding rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    seed_pixels = find_seed_pixels(input_grid)
    
    rows, cols = input_grid.shape

    if len(seed_pixels) > 0:
        #first seed pixel
        r1, c1, v1 = seed_pixels[0]
        output_grid[r1:, c1:] = v1

    if len(seed_pixels) > 1:
        # second seed
        r2, c2, v2 = seed_pixels[1]
        output_grid[:r2+1, :c2+1] = v2
        

    return output_grid.tolist()