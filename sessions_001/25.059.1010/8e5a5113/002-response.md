# 8e5a5113 • 002 • example_3 • investigate_coder

---
```python
"""
1. **Identify Key Regions:** Divide the input grid into three regions: a left block (columns 1-4), a divider column (column 5), and a right block (columns 6-11).

2. **Divider Preservation:** The divider column (all 5s) remains unchanged in the output grid.

3. **Left Block Transformation:**
    - create an empty output_left_block
    - Reverse the *order* of the columns of the input Left block and put into a temp block.
    - For the input left block columns, from left to right, examine pairs of pixels (adjacent colors).
    - Within each horizontal pair, exchange the positions of any two pixels that are *different colors*. If they are the same color, they are not swapped.
    - save the temp block as output_left_block.

4.  **Right Block Transformation:**
    - take columns 6-8 from the right block, reverse the *order* of the columns, and save them to the output_mid_block.
    - Take columns 9-11 of the right block, reverse the *order* of the columns, and exchange each horizontal pair of *different colors* within each row, just like step 3, and save them to the output_right_block.

5. **Combine:** Construct the output grid by combining output_left_block, the original divider column, output_mid_block and output_right_block.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # 1. Identify Key Regions
    left_block = input_grid[:, :4]
    divider_column = input_grid[:, 4:5]
    right_block = input_grid[:, 5:]

    # 2. Divider Preservation (already handled by copying the input grid)

    # 3. Left Block Transformation
    output_left_block = np.copy(left_block[:, ::-1])  # Reverse column order
    for row in range(output_left_block.shape[0]):
      for col in range(0, output_left_block.shape[1] - 1):
          if output_left_block[row,col] != output_left_block[row, col+1]:
              output_left_block[row, col], output_left_block[row, col + 1] = output_left_block[row, col + 1], output_left_block[row, col]


    # 4. Right Block Transformation
    output_mid_block = np.copy(right_block[:, :3][:, ::-1])   # take the first 3 columns and reverse
    output_right_block = np.copy(right_block[:, 3:][:, ::-1]) # Take remaining 3 and reverse
    for row in range(output_right_block.shape[0]):
        for col in range(0, output_right_block.shape[1] - 1):
          if output_right_block[row,col] != output_right_block[row, col+1]:
              output_right_block[row, col], output_right_block[row, col + 1] = output_right_block[row, col + 1], output_right_block[row, col]
    

    # 5. Combine
    output_grid[:, :4] = output_left_block
    output_grid[:, 5:8] = output_mid_block
    output_grid[:, 8:] = output_right_block
    
    return output_grid
```
