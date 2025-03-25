```python
"""
1.  **Find Yellow Blocks:** Identify all contiguous regions of yellow (4) pixels.

2.  **Bounding Boxes:** Determine the bounding box for each yellow region.

3.  **Inner Regions:** Create an "inner region" one pixel smaller on each side of the bounding box. If this creates an invalid inner region (dimensions too small), ignore that yellow block.

4.  **Color Inner Regions:**
    *   **One Yellow Block:**
        *   If any part of the yellow block is in the left half of the grid, color its inner region blue (1).
        *   If any part of the yellow block is in the right half of the grid, color its inner region red (2).
    *   **Multiple Yellow Blocks:**
        *   Color the inner region of the *leftmost* yellow block blue (1).
        *   Color the inner region of the *rightmost* yellow block red (2).
        *   Color the inner regions of any other blocks to the background color (0)

5.  **Output:** Copy the input grid. Replace pixels within valid inner regions with the determined colors.
"""

import numpy as np

def find_contiguous_blocks(grid, color):
    """Finds all contiguous blocks of a specified color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    def dfs(row, col, current_block):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_block.append((row, col))
        dfs(row + 1, col, current_block)
        dfs(row - 1, col, current_block)
        dfs(row, col + 1, current_block)
        dfs(row, col - 1, current_block)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_block = []
                dfs(row, col, current_block)
                blocks.append(current_block)
    return blocks

def get_bounding_box(block):
    """Calculates the bounding box of a block of pixels."""
    rows, cols = zip(*block)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def get_inner_region(bounding_box):
    """Get the inner region for recoloring."""
    min_row, max_row, min_col, max_col = bounding_box

    #one pixel inset
    inner_min_row = min_row + 1
    inner_max_row = max_row - 1
    inner_min_col = min_col + 1
    inner_max_col = max_col - 1

    if inner_min_row > inner_max_row or inner_min_col > inner_max_col:
        return None  # Handle edge case
    
    return inner_min_row, inner_max_row, inner_min_col, inner_max_col

def determine_inner_region_color(yellow_blocks, grid_shape):
    """Determines the color of the inner region based on relative position."""
    colors = []
    if len(yellow_blocks) > 1:
        # Sort blocks by leftmost coordinate (min_col of bounding box)
        sorted_blocks = sorted(yellow_blocks, key=lambda block: get_bounding_box(block)[2])
        
        #the color list must be the same size and order of sorted_blocks
        colors = [0] * len(sorted_blocks)  # Initialize with background color
        
        #Assign colors
        colors[0] = 1  # Leftmost gets blue
        colors[-1] = 2 # Rightmost gets red

    elif len(yellow_blocks) == 1:
        block = yellow_blocks[0]
        bounding_box = get_bounding_box(block)
        min_col = bounding_box[2]
        if min_col < grid_shape[1] / 2:
            colors.append(1)  # Blue
        else:
            colors.append(2)  # Red
    return colors


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)
    yellow_blocks = find_contiguous_blocks(input_grid, 4)
    
    block_colors = determine_inner_region_color(yellow_blocks, input_grid.shape)


    for i, block in enumerate(yellow_blocks):
        bounding_box = get_bounding_box(block)
        inner_region = get_inner_region(bounding_box)

        if inner_region is None: #skips if no inner region
          continue

        inner_min_row, inner_max_row, inner_min_col, inner_max_col = inner_region

        if len(block_colors) > 0:  # Ensure we have a color to use
          new_color = block_colors[i]
          for row in range(inner_min_row, inner_max_row + 1):
            for col in range(inner_min_col, inner_max_col + 1):
              output_grid[row, col] = new_color


    return output_grid
```