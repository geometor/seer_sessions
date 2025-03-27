```python
"""
1.  **Analyze Input Rows:** Examine each row of the input grid independently.
2.  **Identify Color Blocks:** Within each row, identify contiguous, non-zero, same-color blocks. Record the color and length of each block.
3.  **Determine Output Grid Width:**
    *   Calculate the frequency of each block length across *all* rows of the input grid.
    *   The output grid width seems correlated to the most frequent length. Let's refine later if needed.
4.  **Create Output Grid:** Create an output grid with a height of 3 and the width determined in step 3.
5.  **Populate First Output Row:**
    *   Find the first block in the input grid with a length greater than or equal to the output width.  Use its color to fill the *entire* first row of the output. If the input block is longer than the output width, truncate.
6.  **Populate Second Output Row:**
    *  Find the next distinct color block (i.e., different color from the first row) in the input grid (scanning from the beginning) that has a length of at least the output grid width. Use this second block's color to fill the *entire* second row of the output. If the block length in the input exceeds the output width, take the first segment.
7.  **Populate Third Output Row:** Fill the third row of the output grid with zeros (color 0).
"""

import numpy as np
from collections import Counter

def get_blocks_per_row(grid):
    """
    Identifies contiguous non-zero color blocks in each row of the grid.
    Returns a list of lists, where each inner list contains tuples of (color, length) for a row.
    """
    all_rows_blocks = []
    for row in grid:
        row_blocks = []
        current_color = None
        current_block_length = 0
        for pixel in row:
            if pixel != 0:
                if current_color is None:
                    current_color = pixel
                    current_block_length = 1
                elif pixel == current_color:
                    current_block_length += 1
                else:
                    row_blocks.append((current_color, current_block_length))
                    current_color = pixel
                    current_block_length = 1
            elif current_color is not None:
                row_blocks.append((current_color, current_block_length))
                current_color = None
                current_block_length = 0
        if current_color is not None:
            row_blocks.append((current_color, current_block_length))
        all_rows_blocks.append(row_blocks)
    return all_rows_blocks

def determine_output_width(all_rows_blocks):
    """
    Determines the output width based on block length frequencies.
    Prioritizes the first encountered repeated block length.
    """
    block_lengths = []
    for row_blocks in all_rows_blocks:
        for color, length in row_blocks:
            block_lengths.append(length)

    counts = Counter(block_lengths)

    # Iterate through block lengths in order of appearance
    for row_blocks in all_rows_blocks:
      for color, length in row_blocks:
        if counts[length] > 1: # check if a length appears more than once
          return length

    # if we made it this far, check if there are ANY counts
    # this should only happen in a edge or error condition
    if len(counts) > 0:
       return counts.most_common(1)[0][0]

    return 1 # default to 1 if no blocks found (should not happen)



def transform(input_grid):
    # Analyze Input Rows and Identify Color Blocks
    all_rows_blocks = get_blocks_per_row(input_grid)

    # Determine Output Grid Width
    output_width = determine_output_width(all_rows_blocks)

    # Create Output Grid
    output_grid = np.zeros((3, output_width), dtype=int)

    # Populate First Output Row
    first_block_found = False
    for row_blocks in all_rows_blocks:
        for color, length in row_blocks:
            if length >= output_width or (not first_block_found and length>0) :
                output_grid[0, :] = color
                first_block_found = True
                break
        if first_block_found:
            break

    # Populate Second Output Row
    second_block_found = False
    first_color = output_grid[0,0]
    for row_blocks in all_rows_blocks:
        for color, length in row_blocks:
            if (length >= output_width or (not second_block_found and length > 0)) and color != first_color:
                output_grid[1, :] = color
                second_block_found = True
                break
        if second_block_found:
          break

    # Populate Third Output Row (already initialized to zeros)

    return output_grid.tolist()
```