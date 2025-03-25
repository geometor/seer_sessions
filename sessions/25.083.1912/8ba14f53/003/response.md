```python
"""
1.  **Identify Color Blocks:** Scan the first row of the input grid. Identify distinct color blocks, defined as contiguous sequences of the same non-zero color, separated by zeros or the grid boundaries. Note each color found and their respective widths.
2.  **Determine Output Width**: Find the width of the color blocks by counting each of the color blocks up to the `0`.
3.  **Create Output Grid:** Create an output grid with three rows and width determined in step 2.
4.  **Populate Output Rows:**
    *   Fill the first row of the output grid with the pixels of the first identified color block.
    *   Fill the second row of the output grid with the pixels of the second identified color block.
    *   Fill the third row with zeros (color 0).
"""

import numpy as np

def get_color_blocks(grid):
    """
    Identifies distinct colored blocks in the first row and their widths.
    """
    first_row = grid[0, :]
    blocks = []
    current_color = 0
    current_width = 0

    for pixel in first_row:
        if pixel != 0:
            if current_color == 0:
                current_color = pixel
                current_width = 1
            elif pixel == current_color:
                current_width += 1
            elif pixel != current_color:
                blocks.append((current_color, current_width))
                current_color = pixel
                current_width = 1
        elif pixel == 0 and current_color !=0:
            blocks.append((current_color, current_width))
            current_color = 0
            current_width = 0
    if current_color != 0:
      blocks.append((current_color, current_width))

    return blocks

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    blocks = get_color_blocks(input_grid)
    
    # get max width
    max_width = 0
    for block in blocks:
      if block[1] > max_width:
        max_width = block[1]    
    output_grid = np.zeros((3, max_width), dtype=int)

    # build the first row, check if there are any blocks
    if len(blocks) > 0:
        first_color = blocks[0][0]
        width1 = blocks[0][1]
        output_grid[0, :width1] = first_color

    # build the second row
    if len(blocks) > 1:
        second_color = blocks[1][0]
        width2 = blocks[1][1]
        output_grid[1, :width2] = second_color      

    return output_grid.tolist()
```