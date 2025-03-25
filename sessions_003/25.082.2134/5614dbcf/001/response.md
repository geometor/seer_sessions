```python
"""
The input grid is summarized by extracting a single representative digit from each contiguous block of non-white (non-zero) color. The output grid's dimensions are determined by the number of such color blocks. The representative digit is found by checking the center of the block or selecting the first non-zero pixel. Single-pixel regions are ignored.
"""

import numpy as np

def find_color_blocks(grid):
    """Finds contiguous color blocks (excluding white/0) and returns a list of (block, representative_pixel_coords)."""
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    def dfs(row, col, color, current_block):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_block.append((row, col))
        dfs(row + 1, col, color, current_block)
        dfs(row - 1, col, color, current_block)
        dfs(row, col + 1, color, current_block)
        dfs(row, col - 1, color, current_block)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                current_block = []
                dfs(row, col, grid[row, col], current_block)
                if len(current_block) > 1:  # Ignore single-pixel blocks
                    blocks.append(current_block)
    return blocks

def get_representative_pixel(block, grid):
    """Gets the representative pixel coordinates for a block."""
    rows, cols = zip(*block)
    center_row = (min(rows) + max(rows)) // 2
    center_col = (min(cols) + max(cols)) // 2

    if (center_row, center_col) in block:
       return grid[center_row,center_col] # return color value

    # top-left
    for row, col in sorted(block):
        return grid[row,col]

    return None # should not happen, all valid per find_color_blocks


def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    blocks = find_color_blocks(input_grid)
    representative_digits = []

    for block in blocks:
        representative_digit = get_representative_pixel(block, input_grid)
        representative_digits.append(representative_digit)


    # Construct output grid.  Since order matters, just build a list and then
    # reshape
    output_grid_rows = int(np.ceil(np.sqrt(len(representative_digits))))
    output_grid_cols = int(np.ceil(len(representative_digits)/output_grid_rows))

    output_grid = np.zeros((output_grid_rows, output_grid_cols), dtype=int)

    idx = 0
    for r in range(output_grid_rows):
        for c in range(output_grid_cols):
            if idx < len(representative_digits):
                output_grid[r,c] = representative_digits[idx]
                idx+=1

    return output_grid.tolist()
```