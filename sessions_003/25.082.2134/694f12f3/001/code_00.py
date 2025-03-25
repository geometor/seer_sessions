"""
1.  **Identify Yellow Regions:** Locate all contiguous blocks of yellow (4) pixels in the input grid.
2.  **Define Inner Regions:** For each identified yellow region, determine an "inner region".
    *   The inner region starts one pixel inset on each side, from top-left to bottom-right, forming an inner rectangle
3. **Change inner colors:**
    *    If the Yellow block is located in the top-left, change this inner region to blue (1).
    *    If the yellow block is in the bottom-right, change this inner block to red (2)
4.  **Reconstruct Output:** Create the output grid by copying the input grid, then replacing the pixels of each inner region with the newly assigned color (either blue or red), depending on original yellow block location. The locations of the inner regions do not change.
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

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)
    yellow_blocks = find_contiguous_blocks(input_grid, 4)

    for block in yellow_blocks:
        bounding_box = get_bounding_box(block)
        inner_region = get_inner_region(bounding_box)

        if inner_region is None: #skips if no inner region
          continue

        inner_min_row, inner_max_row, inner_min_col, inner_max_col = inner_region

        #Determine color change based on the original yellow block location
        #Check top-left and bottom-right corners to determine block location.

        top_left_corner = (bounding_box[0], bounding_box[2])
        bottom_right_corner = (bounding_box[1], bounding_box[3])
        
        if top_left_corner[0] < output_grid.shape[0] / 2 and top_left_corner[1] < output_grid.shape[1] / 2:
             new_color = 1  # Blue
        elif bottom_right_corner[0] >= output_grid.shape[0] / 2 and bottom_right_corner[1] >= output_grid.shape[1] /2:
             new_color = 2  # Red
        else:
             new_color = None #Should not change

        if new_color is not None:
            for row in range(inner_min_row, inner_max_row + 1):
                for col in range(inner_min_col, inner_max_col + 1):
                    output_grid[row, col] = new_color


    return output_grid