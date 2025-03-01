# 1fad071e • 016 • example_3 • investigate_coder

---
```python
"""
The transformation counts the number of 2x2 blocks of the same color in the input grid and represents these counts in the output grid. The output is a 1xN grid, where N is the number of such 2x2 blocks. Blue (1) square counts are represented by 1 in the output, and other color counts are represented by 0.
"""

import numpy as np

def count_2x2_blocks(input_grid):
    """Counts the number of 2x2 blocks of the same color."""
    count = {0: 0, 1: 0, 2: 0}
    rows, cols = input_grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            block = input_grid[i:i+2, j:j+2]
            if np.all(block == block[0, 0]):
                count[block[0,0]] += 1
    return count

def transform(input_grid):
    # Count the 2x2 blocks of the same color.
    counts = count_2x2_blocks(np.array(input_grid))

    # Create the output grid based on color counts.
    # Blue (1) counts will correspond to 1, others to 0
    output_values = []

    if counts[1] > 0:
      output_values = [1] * counts[1]
    
    if (counts[0] + counts[2]) > 0:
      output_values.append(0)

    # convert to numpy array

    output_grid = np.array(output_values, dtype=int).reshape(1,-1)

    return output_grid
```
