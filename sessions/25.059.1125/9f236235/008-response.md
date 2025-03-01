# 9f236235 • 008 • refine_coder

---
```python
"""
1.  **Identify Green Blocks:** Scan the input grid to identify rectangular blocks of green (3) pixels. The minimum size of these blocks is 2x2.
2.  **Determine Relative Position:** Divide the input grid conceptually into four equal sections, creating a 2x2 layout of sections (not necessarily quadrants based on the center, but partitions of the height and width).
3. **Map to Output:** For each identified green block, extract the value of its top-left pixel. Place this value in the output grid at the position corresponding to the section the green block's top-left pixel falls within. For example, if a block falls within the upper-left partition of input, its pixel value should be placed in output at [0,0]. The input appears to be partitioned at height / 2 and width / 2
4.  **Output Grid:** The output grid is always 4x4. If no green blocks are found in an input partition, the corresponding output cell should be 0 (white).
"""

import numpy as np

def find_green_blocks(grid):
    # Find 2x2 or larger green blocks.
    green_blocks = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            if grid[r, c] == 3:  # Check for green pixel
                # Expand to find largest possible block
                max_row = height
                max_col = width
                
                for r2 in range(r+1, height):
                  if grid[r2,c] != 3:
                    max_row = r2
                    break

                for c2 in range(c+1, width):
                  if grid[r, c2] != 3:
                    max_col = c2
                    break

                
                block = grid[r:max_row, c:max_col]

                if block.shape[0] >= 2 and block.shape[1] >= 2 and np.all(block == 3) :
                    green_blocks.append((r, c))

    return green_blocks

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the green blocks
    green_blocks = find_green_blocks(input_grid)

    # Determine output grid size and initialize
    output_size = 4
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Map green blocks to output grid
    for r, c in green_blocks:
        # Determine the relative position (section) of the green block
        row_index = 0 if r < (input_grid.shape[0] / 2) else 1
        col_index = 0 if c < (input_grid.shape[1] / 2) else 1

        row_index *= 2
        col_index *= 2

        # Get the top-left pixel value of block
        pixel_value = input_grid[r, c]

        output_grid[row_index, col_index] = pixel_value

    return output_grid
```
