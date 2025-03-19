# 1f85a75f • 010 • example_2 • investigate_coder

---
```python
"""
Finds the largest contiguous block of color 4 (yellow) pixels within the input grid and replicates it as the output grid.
"""

import numpy as np

def find_largest_yellow_block(grid):
    """
    Finds the largest contiguous block of yellow (color 4) pixels in a grid.
    Returns the bounding box coordinates (row_start, col_start, row_end, col_end) of the block.
    If no yellow block is found, it may need to return some default/error condition
    but it seems there's always at least one yellow cell in the ARC tasks.
    """
    rows, cols = grid.shape
    max_size = 0
    best_block = None

    for row_start in range(rows):
        for col_start in range(cols):
            if grid[row_start, col_start] == 4:  # Start of a potential block
                # Explore the block
                row_end = row_start
                col_end = col_start

                # Expand downwards as far as possible
                while row_end + 1 < rows and grid[row_end + 1, col_start] == 4:
                    row_end += 1

                # Expand rightwards as far as possible
                while col_end + 1 < cols and all(grid[row_start:row_end + 1, col_end + 1] == 4):
                    col_end += 1
                
                #check for complete block.
                current_size = (row_end - row_start + 1) * (col_end - col_start + 1)
                all_yellow = True
                for r in range(row_start,row_end + 1):
                    for c in range(col_start,col_end + 1):
                        if grid[r,c] != 4:
                            all_yellow = False
                            break
                    if not all_yellow:
                        break

                if all_yellow:
                    if current_size > max_size:
                        max_size = current_size
                        best_block = (row_start, col_start, row_end, col_end)


    return best_block

def transform(input_grid):
    """
    Transforms the input grid by extracting the largest yellow block.
    """
    # Find the largest yellow block
    block_coords = find_largest_yellow_block(np.array(input_grid))

    if block_coords is None:
        return [[]]

    row_start, col_start, row_end, col_end = block_coords

    # Create the output grid based on block size
    output_grid = np.full((row_end - row_start + 1, col_end - col_start + 1), 4, dtype=int)

    return output_grid.tolist()
```
