```python
"""
1.  **Iterate through Columns:** Process the grid column by column.
2.  **Locate Seed Yellow:** Within each column, search for the *topmost* yellow (4) pixel. This is our "seed" for the downward fill.
3.  **Conditional Downward Fill:**
    *   If a seed yellow pixel is found, examine the pixels *directly below* it in the same column.
    *   If a pixel below is white (0), change it to yellow (4).
    *    Continue this downward filling for all continuous white pixels until either a non-white pixel or the bottom of the grid is encountered.
4.  **Preserve Input Pixels:** Pixels not meeting the criteria above are copied from input to output without changes.
5.  **Grid size constant**: Maintain the grid size across the transformation.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each column
    for j in range(cols):
        # Find the topmost yellow pixel in the column
        seed_yellow_row = -1
        for i in range(rows):
            if input_grid[i][j] == 4:
                seed_yellow_row = i
                break  # Found the topmost, so stop searching

        # Conditional Downward Fill
        if seed_yellow_row != -1:
            for i in range(seed_yellow_row, rows):
                if output_grid[i][j] == 0:
                    output_grid[i][j] = 4
                elif output_grid[i][j] != 0 and i > seed_yellow_row:
                  break


    return output_grid
```