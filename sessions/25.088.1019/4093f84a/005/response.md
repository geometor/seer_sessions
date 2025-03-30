```python
import numpy as np

"""
Transformation Rule Natural Language Description:

1.  **Initialization**: Create the output grid as an identical copy of the input grid.
2.  **Identify Band Boundaries**:
    *   Find the smallest row index (`band_top_row`) that contains at least one gray (5) pixel.
    *   Find the largest row index (`band_bottom_row`) that contains at least one gray (5) pixel.
    *   If no gray pixels exist, skip modification steps and proceed directly to cleanup (Step 5).
3.  **Process Area Above Band**:
    *   If a gray band exists (`band_top_row != -1`):
        *   Identify all columns (`c`) where at least one active pixel (blue=1, red=2, or green=3) exists in any row *above* `band_top_row` (i.e., row index `< band_top_row`) in the *input* grid.
        *   For each such identified column `c`, change the color of the pixel in the output grid at position (`band_top_row`, `c`) to gray (5).
4.  **Process Area Below Band**:
    *   If a gray band exists (`band_bottom_row != -1`):
        *   Identify all columns (`c`) where at least one active pixel (blue=1, red=2, or green=3) exists in any row *below* `band_bottom_row` (i.e., row index `> band_bottom_row`) in the *input* grid.
        *   For each such identified column `c`, change the color of the pixel in the output grid at position (`band_bottom_row`, `c`) to gray (5).
5.  **Cleanup Active Colors**:
    *   Iterate through every pixel (`r`, `c`) of the potentially modified output grid.
    *   If the pixel's color is currently blue (1), red (2), or green (3), change its color to white (0).
6.  **Final Output**: The resulting grid after the cleanup step is the final output.
"""

def find_band_boundaries(grid):
    """
    Finds the indices of the first (top) and last (bottom) rows
    containing a gray (5) pixel.
    Returns (band_top_row, band_bottom_row) or (-1, -1) if no gray pixel is found.
    """
    gray_color = 5
    # Find row indices where any cell in the row is gray
    gray_rows = np.where(np.any(grid == gray_color, axis=1))[0]
    if len(gray_rows) == 0:
        return -1, -1  # No gray pixels found
    else:
        # Return the minimum and maximum row index containing gray
        return gray_rows.min(), gray_rows.max()

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    - Finds the top and bottom rows of the gray band.
    - Identifies columns with active colors (1, 2, 3) above and below the band.
    - Colors the cell *on* the top/bottom band row gray in those columns.
    - Replaces all remaining active colors (1, 2, 3) with white (0).
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np) # Start with a copy
    height, width = input_np.shape
    
    active_colors = {1, 2, 3} # Blue, Red, Green
    gray_color = 5
    white_color = 0

    # 1. Find the band boundaries
    band_top_row, band_bottom_row = find_band_boundaries(input_np)

    # Only proceed with modifications if a band exists
    if band_top_row != -1: # Check if any gray was found

        # 2. Process Area Above Band
        # Identify columns with active colors above the band
        cols_to_modify_above = set()
        # Iterate through columns
        for c in range(width):
            # Check rows from 0 up to (but not including) band_top_row
            for r in range(band_top_row):
                if input_np[r, c] in active_colors:
                    cols_to_modify_above.add(c)
                    break # Found one active color in this column above the band, move to the next column
        
        # Modify the pixels *on* the top band row in identified columns
        target_row_above = band_top_row
        for c in cols_to_modify_above:
            # Check if the target row is valid (it should be if band_top_row != -1)
            if 0 <= target_row_above < height:
                 output_np[target_row_above, c] = gray_color

        # 3. Process Area Below Band
        # Identify columns with active colors below the band
        cols_to_modify_below = set()
        # Iterate through columns
        for c in range(width):
            # Check rows from band_bottom_row + 1 down to the last row
            for r in range(band_bottom_row + 1, height):
                 if input_np[r, c] in active_colors:
                    cols_to_modify_below.add(c)
                    break # Found one active color in this column below the band, move to the next column

        # Modify the pixels *on* the bottom band row in identified columns
        target_row_below = band_bottom_row
        for c in cols_to_modify_below:
             # Check if the target row is valid (it should be if band_bottom_row != -1)
             if 0 <= target_row_below < height:
                output_np[target_row_below, c] = gray_color

    # 4. Cleanup Active Colors - Iterate through the *output* grid after modifications
    for r in range(height):
        for c in range(width):
            # If a pixel is still an active color (blue, red, or green)
            if output_np[r, c] in active_colors:
                output_np[r, c] = white_color # Change it to white

    # Convert the result back to a standard list of lists for the ARC environment
    return output_np.tolist()
```