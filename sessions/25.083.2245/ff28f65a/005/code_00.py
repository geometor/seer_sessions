"""
1.  **Input:** A 2D grid (`input_grid`).
2.  **Output:** A 3x3 grid (`output_grid`) initialized with all zeros.
3.  **Find 2x2 Red Blocks:** Locate all 2x2 blocks within the `input_grid` where all four cells are red (value 2). Store the top-left coordinates of these blocks.
4.  **Divide into Regions:** Divide the `input_grid` into nine overlapping regions.  The size of each region to check for blocks depends on the height and width of the input grid. Each dimension (height, width) is divided into thirds: `row_thirds = rows // 3`, `col_thirds = cols // 3`.
5. **Determine Output Grid Values.** The output grid (3x3) corresponds to checking the input grid divided into thirds. The regions within the input grid are defined as follows, clamping the end values to the height and width of the grid respectively:
    *   For each cell (out_row, out_col) in the `output_grid` (from 0 to 2):
        *   `row_start = out_row * row_thirds`
        *   `row_end = min((out_row + 1) * row_thirds, rows)`
        *   `col_start = out_col * col_thirds`
        *   `col_end = min((out_col + 1) * col_thirds, cols)`
        *   Check if *any* of the 2x2 red blocks found in Step 3 have their top-left corner coordinates within the current region defined by `row_start`, `row_end`, `col_start`, and `col_end`.
        *   If a red block's top-left corner is found within the region, set `output_grid[out_row, out_col] = 1`.
        *   Otherwise, `output_grid[out_row, out_col]` remains 0.
6.  **Return:** The 3x3 `output_grid`.
"""

import numpy as np

def find_2x2_blocks(grid, color):
    """Finds all 2x2 blocks of the specified color in the grid."""
    blocks = []
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i:i+2, j:j+2] == color).all():
                blocks.append((i, j))  # Store top-left corner coordinates
    return blocks

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Calculate row and column thirds
    row_thirds = rows // 3
    col_thirds = cols // 3

    # Scan for Red Blocks
    red_blocks = find_2x2_blocks(input_grid, 2)

    # Determine output based on regions
    for out_row in range(3):
        for out_col in range(3):
            row_start = out_row * row_thirds
            row_end = min((out_row + 1) * row_thirds, rows) #clamp to height
            col_start = out_col * col_thirds
            col_end = min((out_col + 1) * col_thirds, cols) #clamp to width

            for block_row, block_col in red_blocks:
                if row_start <= block_row < row_end and col_start <= block_col < col_end:
                    output_grid[out_row, out_col] = 1
                    break  # Once a block is found in the region, set to 1 and move to next

    return output_grid.tolist()