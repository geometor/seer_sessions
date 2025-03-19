"""
1.  **Identify the Seed:** Find the single orange (7) pixel in the input grid. Note its row (`r`) and column (`c`).
2.  **Create the Expanded Block:** Create a 3x3, 2x3, or 1x3 block of orange (7) pixels in the output grid.
3. **Determine if more rows are needed:** if the seed pixel is not on row 0 or 1, add rows above, so the output is 3 rows.
4.  **Position the Expanded Block:** The expanded blocks first orange pixel column will match the seed pixel's column (`c`). Add two additional orange pixels to the right, at `c+1` and `c+2`
5.  **Preserve Non-Orange Pixels:** This part is implicit, but crucial. All other pixels in the input grid that are *not* the seed orange pixel should remain unchanged in the output grid (their color and position stay the same). Since all the examples only have black and orange, the code should assume this and change later if needed.
"""

import numpy as np

def find_seed_pixel(grid):
    # Find the coordinates of the orange pixel (7).
    orange_pixels = np.where(grid == 7)
    if len(orange_pixels[0]) > 0:
        return orange_pixels[0][0], orange_pixels[1][0]  # Return row, col
    else:
        return None  # No orange pixel found

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = input_grid.copy()
    
    # Find the seed pixel (the single orange pixel).
    seed_location = find_seed_pixel(input_grid)

    if seed_location:
        seed_row, seed_col = seed_location

        # Determine the starting row for the expanded block
        start_row = max(0, seed_row - (2-seed_row)) #ensure the are three total rows of orange
        if start_row<0:
          start_row = 0

        # Apply expansion, ensure bounds
        for r in range(start_row, seed_row + 2): #up to three total rows of orange
            for c in range(seed_col, min(seed_col + 3, output_grid.shape[1])): #max three cols
                if r>=0 and r < output_grid.shape[0]: #check row and column
                  output_grid[r, c] = 7

    return output_grid