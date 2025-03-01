# 662c240a • 002 • example_4 • investigate_coder

---
```python
"""
The input is a 9x3 grid.  The output is a 3x3 sub-block of the input grid.
The output grid is the first 3x3 block in the input that contains all unique values, when scanned from top to bottom.
"""

import numpy as np

def get_3x3_blocks(grid):
    """Splits a 9x3 grid into three 3x3 blocks."""
    blocks = []
    for i in range(0, 9, 3):
        blocks.append(grid[i:i+3, :])
    return blocks

def has_unique_values(block):
    """Checks if a 3x3 block has all unique values."""
    flattened = block.flatten()
    return len(np.unique(flattened)) == 9

def transform(input_grid):
    """
    Selects a 3x3 block from the input grid based on uniqueness criteria.
    """
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)
    
    # Get the 3x3 blocks
    blocks = get_3x3_blocks(input_grid)

    # Select the first block with unique values
    output_grid = None
    for block in blocks:
      if has_unique_values(block):
        output_grid = block
        break
    
    if output_grid is None:
      for block in blocks:
        flattened = block.flatten()
        if len(np.unique(flattened)) > 1: #check for multiple values
          output_grid = block
          break

    if output_grid is None:  #if still none, take the top block
      output_grid = blocks[0]

    return output_grid.tolist()
```
