# f35d900a • 026 • refine_coder

---
```python
"""
Transforms an input grid containing isolated green (3) and azure (8) pixels by:

1. Expanding each green and azure pixel into a 3x3 block of the same color, centered on the original pixel's location.
2. Merging overlapping expanded blocks of the same color.
3. Connecting the *nearest* expanded blocks of different colors (green and azure) with a horizontal path of grey (5) pixels.  The path starts from the right edge of the green block and extends to the left edge of the azure block.
4. The connection path lies on the row that is the vertical center of the green block.
5. All other pixels are white (0).
"""

import numpy as np

def expand_and_merge(grid, color_value):
    """Expands pixels of a given color into 3x3 blocks and merges overlapping blocks."""
    rows, cols = grid.shape
    expanded_grid = np.zeros_like(grid)

    # Expand each pixel
    for r, c in np.argwhere(grid == color_value):
        for i in range(max(0, r - 1), min(rows, r + 2)):
            for j in range(max(0, c - 1), min(cols, c + 2)):
                expanded_grid[i, j] = color_value

    # Merge by re-finding contiguous blocks after expansion
    merged_grid = np.zeros_like(expanded_grid)
    visited = np.zeros_like(expanded_grid, dtype=bool)
    block_coords = []

    def dfs(r, c):
        """Depth-first search to find contiguous blocks."""
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            visited[r, c] or merged_grid[r,c] != color_value):
            return []

        visited[r, c] = True
        coords = [(r, c)]
        coords.extend(dfs(r + 1, c))
        coords.extend(dfs(r - 1, c))
        coords.extend(dfs(r, c + 1))
        coords.extend(dfs(r, c - 1))
        return coords

    for r in range(rows):
      for c in range(cols):
        if expanded_grid[r,c] == color_value and not visited[r,c]:
            block = dfs(r,c)
            if block:
                block_coords.append(block)
                for br,bc in block:
                  merged_grid[br,bc] = color_value

    return merged_grid, block_coords
    

def get_block_extrema(block_coords):
    """Calculates the leftmost, rightmost, topmost, and bottommost coordinates of a block."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for r, c in block_coords:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def connect_blocks(grid, green_block, azure_block):
    """Connects two blocks with a horizontal grey path, if they don't overlap."""
    _, _, _, green_max_c = get_block_extrema(green_block)
    _, azure_min_c, _, _ = get_block_extrema(azure_block)

    # Find the center row of the green block
    green_min_r, _, green_max_r, _ = get_block_extrema(green_block)
    green_center_row = (green_min_r + green_max_r) // 2

    if green_max_c < azure_min_c:  # Check for overlap
        for c in range(green_max_c + 1, azure_min_c):
            grid[green_center_row, c] = 5



def transform(input_grid):
    # Initialize output_grid to all white
    output_grid = np.zeros_like(input_grid)

    # Expand and merge green blocks
    expanded_green_grid, green_blocks = expand_and_merge(input_grid, 3)
    for blk in green_blocks:
      for r,c in blk:
        output_grid[r,c] = 3 # set the merged green blocks

    # Expand and merge azure blocks
    expanded_azure_grid, azure_blocks = expand_and_merge(input_grid, 8)
    for blk in azure_blocks:
      for r,c in blk:
        output_grid[r,c] = 8 # set the merged azure blocks


    # connect
    for green_block in green_blocks:
        nearest_azure_block = None
        min_dist = float('inf')

        for azure_block in azure_blocks:
            _, _, _, green_max_c = get_block_extrema(green_block)
            _, azure_min_c, _, _ = get_block_extrema(azure_block)
            dist = azure_min_c - green_max_c  # Horizontal distance

            if 0 < dist < min_dist: # the distance needs to be positive
                min_dist = dist
                nearest_azure_block = azure_block

        if nearest_azure_block:
            connect_blocks(output_grid, green_block, nearest_azure_block)
    return output_grid
```
