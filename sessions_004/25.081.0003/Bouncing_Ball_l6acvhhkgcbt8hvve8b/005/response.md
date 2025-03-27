```python
"""
1.  **Identify Objects:** Locate all yellow (4) and red (2) pixels in the input grid.
2.  **Conditional Swap:**
    *   If all yellow and red pixels are in the *same column*, and all yellow pixels are *above* all red pixels, *do not* perform a swap. The output is identical to the input.
    *   Otherwise, perform a swap:
        * Find the top-most row index containing yellow pixels, call this `top_yellow_row`.
        * Find the bottom-most row index containing red pixels. call this 'bottom_red_row`.
        * Conceptually move all yellow pixels as a block down such that the top of the yellow block is now at the bottom of the old red block. The new y positions for yellow is calculated `new_yellow_row = bottom_red_row - (original_yellow_row - top_yellow_row)`
        * Move all of the red pixels, as a block up, such that the bottom of the red block is now at the location of the top most yellow block. The new y position for the red pixels will be calculated: `new_red_row = top_yellow_row + (bottom_red_row - original_red_row)`.

3. **Clear and Fill**: Before performing the swap as described above, first set all of the yellow and red pixels in the output grid to black(0). Then perform the swap as described above.
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the coordinates of pixels of a specific color."""
    return [(r, c) for r in range(grid.shape[0]) for c in range(grid.shape[1]) if grid[r, c] == color]

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Identify Objects
    yellow_pixels = find_pixels(input_grid, 4)
    red_pixels = find_pixels(input_grid, 2)

    # Conditional Swap
    if yellow_pixels and red_pixels:
        # Check if all yellow and red pixels are in the same column and yellow is above red
        same_column = all(y[1] == yellow_pixels[0][1] for y in yellow_pixels) and all(r[1] == red_pixels[0][1] for r in red_pixels)
        if same_column:
            all_yellow_above_red = True
            for y_row, _ in yellow_pixels:
                for r_row, _ in red_pixels:
                    if y_row >= r_row:
                        all_yellow_above_red = False
                        break
                if not all_yellow_above_red:
                    break

        if same_column and all_yellow_above_red:
             return output_grid  # No swap
        
        #Clear all yellow and red
        for r,c in yellow_pixels:
            output_grid[r,c] = 0

        for r,c in red_pixels:
            output_grid[r,c] = 0

        # proceed with the swap
        top_yellow_row = min(y[0] for y in yellow_pixels)
        bottom_red_row = max(r[0] for r in red_pixels)

        # Move yellow pixels
        for y_row, y_col in yellow_pixels:
            new_yellow_row = bottom_red_row - (y_row - top_yellow_row)
            output_grid[new_yellow_row, y_col] = 4

        # Move red pixels
        for r_row, r_col in red_pixels:
            new_red_row = top_yellow_row + (bottom_red_row - r_row)
            output_grid[new_red_row, r_col] = 2

    return output_grid
```