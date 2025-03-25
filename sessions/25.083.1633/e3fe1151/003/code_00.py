"""
1.  **Background:** Identify color 7 (orange) as the background. Pixels with this color remain unchanged.

2.  **Center:** Identify the central row and column (index 2 in a 5x5 grid).

3. **Center Row and Column Transformations:**
    - Center Row: No changes.
    - Center Column:
        - If input=3 and row < center: output=2
        - if input=3 and row > center: output=4
        - if input=7 output=7
        - if input = 9, output = 9
        - if input = 4 and row < center output = 4
        - if input = 4 and row > center, output = 4
        - if input = 5, output = 5

4.  **Positional Transformations (Non-Center):**

    *   **Top Row (r=0):**
        If Input=1, Output=5.
        If Input=8, Output=0.

    *   **Bottom Row (r=4):**
        If Input=1, Output=5
        If Input=8, output=0.

    *   **Left Column (c=0):**
      if input = 8, output=0
    *  **Second Row (r=1):**
        - If Input=8 and c<center_col, Output=0
        - If Input=1 and c>center_col, Output=5
    *  **Fourth Row (r=3):**
       - If Input=8 and c< center_col, output =8
       - If input=1 and c> center_col, output=0
    * **Second Column**
      - if input = 1, output = 1
    *  **Fourth Column:**
        -if input=8, output=5

5.  **Output:** Create the output grid by applying the above transformations while preserving the background color (7).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_row = rows // 2
    center_col = cols // 2

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            # Background remains unchanged
            if input_grid[r, c] == 7:
                continue

            # Center Column Transformations
            if c == center_col:
                if input_grid[r, c] == 3 and r < center_row:
                    output_grid[r, c] = 2
                elif input_grid[r, c] == 3 and r > center_row:
                    output_grid[r, c] = 4
                elif input_grid[r,c] == 9:
                    output_grid[r,c] = 9
                elif input_grid[r,c] == 4:
                    output_grid[r,c] = 4
                elif input_grid[r, c] == 5:
                    output_grid[r, c] = 5

            # Positional Transformations (Non-Center)
            else:
                if r == 0:
                    if input_grid[r, c] == 1:
                        output_grid[r, c] = 5
                    elif input_grid[r, c] == 8:
                        output_grid[r, c] = 0
                elif r == 4:
                    if input_grid[r, c] == 1:
                        output_grid[r, c] = 5
                    elif input_grid[r, c] == 8:
                        output_grid[r, c] = 0
                elif c == 0:
                    if input_grid[r,c] == 8:
                        output_grid[r,c] = 0

                elif r == 1:
                    if input_grid[r, c] == 8 and c < center_col:
                        output_grid[r, c] = 0
                    elif input_grid[r, c] == 1 and c > center_col:
                        output_grid[r, c] = 5
                elif r == 3:
                    if input_grid[r,c] == 8 and c < center_col:
                        output_grid[r,c] = 8
                    elif input_grid[r,c] == 1 and c > center_col:
                        output_grid[r,c] = 0

                elif c == 1:
                    if input_grid[r,c] == 1:
                        output_grid[r,c] = 1
                elif c==3:
                    if input_grid[r,c] == 8:
                        output_grid[r,c] = 5

    return output_grid