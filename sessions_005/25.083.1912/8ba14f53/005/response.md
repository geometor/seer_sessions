```python
"""
1.  **Examine Input:** Examine the input grid, identifying all contiguous, non-zero, same-color blocks, in all rows.
2.  **Block Length:** Determine the most frequent color block size within the entire input grid.
3.  **Output Dimensions:** Create an output grid with a height of 3 and a width equal to the block length identified in Step 2.
4.  **Populate Output:**
    *   Locate the first color block in the input grid. Copy this block to the first row of the output grid.
    *   Locate the second color block in the input grid. Copy this block to the second row of the output grid.
    *   Fill the third row of the output grid with zeros (color 0).
"""

import numpy as np
from collections import Counter

def get_all_color_blocks(grid):
    """
    Identifies all contiguous non-zero color blocks in the grid.
    """
    blocks = []
    for row in grid:
        current_color = None
        current_block = []
        for pixel in row:
            if pixel != 0:
                if current_color is None:
                    current_color = pixel
                    current_block.append(pixel)
                elif current_color == pixel:
                    current_block.append(pixel)
                else:
                    blocks.append((current_color, len(current_block)))
                    current_color = pixel
                    current_block = [pixel]
            elif current_color is not None:
                blocks.append((current_color, len(current_block)))
                current_color = None
                current_block = []
        if current_color is not None:
            blocks.append((current_color, len(current_block)))
    return blocks

def get_block_length(blocks):
  """
  find the most common block length
  """
  block_lengths = [block[1] for block in blocks]

  # count them
  counts = Counter(block_lengths)

  # if there are any counts
  if len(counts) > 0:
    return counts.most_common(1)[0][0]
  else:
    return 0

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    blocks = get_all_color_blocks(input_grid)
    block_length = get_block_length(blocks)
    
    output_grid = np.zeros((3, block_length), dtype=int)

    # build the first row, check if any blocks exist
    if len(blocks) > 0:
        first_color = blocks[0][0]
        output_grid[0, :block_length] = first_color

    # build the second row
    if len(blocks) > 1:
        second_color = blocks[1][0]
        output_grid[1, :block_length] = second_color

    return output_grid.tolist()
```