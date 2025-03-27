"""
1.  **Input Grouping:** Divide the input grid into 3x3 blocks, starting from the top-left corner. Overlapping is allowed, meaning we process every possible 3x3 square within the input.
2.  **Color Selection:** Within each 3x3 block, identify all unique colors present (excluding 0, the background).
3.  **Output Grid Creation:** Create an output grid. The dimensions will be based on condensing every 3 rows and 3 columns into 1.
4.  **Output Population:**
    *   For each 3x3 block in the input:
        *   Determine the corresponding position in the output grid (row index divided by 3, column index divided by 3). Integer division.
        *   If the 3x3 block contains any non-zero colors, place those *unique* colors into the output grid.
        * If there are more than one, try placing all non zero unique colors.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = (rows + 2) // 3  # Integer division, rounding up
    output_cols = (cols + 2) // 3  # Integer division, rounding up
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through all possible 3x3 blocks
    for i in range(rows):
        for j in range(cols):
            # Define the 3x3 block
            block = input_grid[i:min(i + 3, rows), j:min(j + 3, cols)]
            
            # Find unique non-zero colors in the block
            unique_colors = np.unique(block[block != 0])

            # Determine output position
            output_row = i // 3
            output_col = j // 3

            # Place unique colors into the output grid
            if len(unique_colors) > 0:
                output_grid[output_row, output_col] = unique_colors[0]  #place the first

    return output_grid.tolist()