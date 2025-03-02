# ea32f347 • 020 • refine_coder

---
```python
"""
1.  **Identify Gray Blocks:** Locate all contiguous regions of gray (5) pixels within the input grid.

2.  **Classify Orientation:** For each identified gray block, determine its orientation:
    *   **Horizontal:** If the block is wider than it is tall.
    *   **Vertical:** If the block is taller than it is wide.

3.  **Recolor Vertical Blocks:** Transform all pixels within vertical gray blocks to yellow (4).

4.  **Recolor Horizontal Blocks:**
    *   Identify sets of *vertically stacked* horizontal gray blocks. Blocks are considered stacked if they have at least one pixel in the same column and are either adjacent or separated only by rows of non-gray pixels.
    *    Within each stack:
        *   Recolor the **topmost** horizontal block to blue (1).
        *   Recolor the **bottommost** horizontal block to red (2).
        *    Blocks that are neither top nor bottom remain unchanged.

5.  **Preserve Other Colors:** Ensure that all pixels which were not part of a gray block in the input grid retain their original colors.
"""

import numpy as np

def find_contiguous_blocks(grid, color):
    # Find contiguous blocks of a given color in the grid.
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    def dfs(r, c, current_block):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_block.append((r, c))
        dfs(r + 1, c, current_block)
        dfs(r - 1, c, current_block)
        dfs(r, c + 1, current_block)
        dfs(r, c - 1, current_block)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_block = []
                dfs(r, c, current_block)
                blocks.append(current_block)
    return blocks

def classify_orientation(block):
    # Classify the orientation of a block as horizontal or vertical.
    rows, cols = zip(*block)
    height = max(rows) - min(rows) + 1
    width = max(cols) - min(cols) + 1
    return "horizontal" if width > height else "vertical"

def are_blocks_stacked(block1, block2, grid):
    # Check if two horizontal blocks are vertically stacked.
    cols1 = set([c for r, c in block1])
    cols2 = set([c for r, c in block2])

    # Check for shared columns
    if not cols1.intersection(cols2):
        return False

    # get rows and sort
    rows1 = sorted(list(set([r for r,c in block1])))
    rows2 = sorted(list(set([r for r,c in block2])))
   
    # Check for adjacency or separation by non-gray pixels
    if rows1[-1] < rows2[0]: # block 1 is above
      for r in range(rows1[-1] + 1, rows2[0]):
        for c in cols1.intersection(cols2):
          if grid[r,c] == 5:
            return False # separated by gray
      return True
    elif rows2[-1] < rows1[0]:
      for r in range(rows2[-1] + 1, rows1[0]): # block 2 is above
        for c in cols1.intersection(cols2):
          if grid[r,c] == 5:
            return False
      return True
          
    return False

def get_stacked_horizontal_blocks(horizontal_blocks, grid):
    # Group horizontal blocks into vertically stacked sets.
    stacked_sets = []
    processed = [False] * len(horizontal_blocks)

    for i in range(len(horizontal_blocks)):
        if not processed[i]:
            current_stack = [horizontal_blocks[i]]
            processed[i] = True
            for j in range(i + 1, len(horizontal_blocks)):
                if not processed[j]:
                    for block in current_stack:
                        if are_blocks_stacked(block, horizontal_blocks[j], grid):
                            current_stack.append(horizontal_blocks[j])
                            processed[j] = True
                            break  # Move to the next block after finding a match
            stacked_sets.append(current_stack)
    return stacked_sets

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    gray_blocks = find_contiguous_blocks(output_grid, 5)

    # get horizontal and vertical blocks
    horizontal_blocks = []
    for block in gray_blocks:
        if classify_orientation(block) == "vertical":
            for r, c in block:
                output_grid[r,c] = 4 # recolor vertical
        else:
          horizontal_blocks.append(block)

    # get stacked sets
    stacked_sets = get_stacked_horizontal_blocks(horizontal_blocks, output_grid)

    # recolor horizontal based on stacking
    for stack in stacked_sets:
      if len(stack) > 0:
        # find min and max rows - top and bottom
        min_row = min([min(list(zip(*block))[0]) for block in stack])
        max_row = max([max(list(zip(*block))[0]) for block in stack])

        for block in stack:
          block_min_row = min(list(zip(*block))[0])
          # recolor top and bottom
          if block_min_row == min_row:
            for r, c in block:
              output_grid[r,c] = 1 # top
          elif block_min_row == max_row:
            for r,c in block:
              output_grid[r,c] = 2  # bottom
          # else leave the same

    return output_grid
```
