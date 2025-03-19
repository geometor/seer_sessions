# 3bdb4ada • 002 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to identify contiguous horizontal blocks of the same color in each row of the input grid. 
Then, for every other block in a group of blocks on the same row with same color, 
insert a background pixel (0) at every other position within the block, starting from the second pixel.
"""

import numpy as np

def find_blocks(row):
    """Finds contiguous blocks of non-zero pixels in a row."""
    blocks = []
    in_block = False
    start = 0
    for i, pixel in enumerate(row):
        if pixel != 0:
            if not in_block:
                in_block = True
                start = i
        elif in_block:
            in_block = False
            blocks.append((start, i - 1, row[start]))
    if in_block:
        blocks.append((start, len(row) - 1, row[start]))
    return blocks

def checker_block(block, row):
    """Modifies a block by inserting 0 at every other position, in place."""
    start, end, color = block
    for i in range(start + 1, end + 1, 2):
        row[i] = 0

def transform(input_grid):
    """Transforms the input grid according to the checkerboard rule."""
    output_grid = np.copy(input_grid)
    rows = len(input_grid)

    for row_index in range(rows):
      blocks = find_blocks(input_grid[row_index])
      block_groups = {}  #group by color
      for block in blocks:
          color = block[2]
          if color not in block_groups:
              block_groups[color] = []
          block_groups[color].append(block)
      
      for color, blocks_of_color in block_groups.items():
          for i,block in enumerate(blocks_of_color):
              if (i % 2) != 0:  #check if the block is at an odd index within blocks of same color
                  checker_block(block, output_grid[row_index])
    return output_grid
```
