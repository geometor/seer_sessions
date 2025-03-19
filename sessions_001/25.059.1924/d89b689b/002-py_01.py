"""
1. **Identify and Remove Blocks:** Scan the input grid to identify 2x2 blocks of azure (color 8). Remove these blocks entirely.
2. **Identify single colored pixels:** Identify all single colored pixels in the input grid (pixels which do not belong to any multi pixel block).
3. **Reposition Pixels**: Take the identified single colored pixels and arrange them into a 2x2 block in the center of the output grid. Fill the single pixels starting with the top row from left to right, and then the next row from left to right. Any remaining cell of the 2x2 block at the output are filled with 0.
4. Set the rest of the cell in output grid to 0.
"""

import numpy as np

def find_2x2_blocks(grid, color):
    blocks = []
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            if (grid[r, c] == color and grid[r + 1, c] == color and
                grid[r, c + 1] == color and grid[r + 1, c + 1] == color):
                blocks.append((r, c))
    return blocks

def find_single_pixels(grid):
    single_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 0: continue

            is_single = True
            # Check neighbors (including diagonals)
            for i in range(max(0, r - 1), min(rows, r + 2)):
                for j in range(max(0, c - 1), min(cols, c + 2)):
                    if (i, j) != (r, c) and grid[i, j] == grid[r,c]:
                        is_single = False
                        break
                if not is_single:
                    break
            if is_single:    
                single_pixels.append((r, c, grid[r,c]))

    return single_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Identify and Remove Blocks
    azure_blocks = find_2x2_blocks(input_grid, 8)
    temp_grid = input_grid.copy()
    for r, c in azure_blocks:
        temp_grid[r:r+2, c:c+2] = 0

    # Identify single colored pixels
    single_pixels = find_single_pixels(temp_grid)
    
    # Reposition Pixels
    center_row = rows // 2
    center_col = cols // 2

    pixel_positions = [
        (center_row -1, center_col -1),
        (center_row -1, center_col),
        (center_row, center_col - 1),
        (center_row, center_col)
    ]

    for i in range(min(len(single_pixels), 4)):
        row, col = pixel_positions[i]
        output_grid[row, col] = single_pixels[i][2] #place color value

    return output_grid