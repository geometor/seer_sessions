# 7447852a • 002 • example_3 • investigate_coder

---
```python
"""
Iterate through each row of the input grid. Within each row, locate the white (0) pixels that are horizontally adjacent to the right of a sequence of red (2) pixels. Replace those white (0) pixels with yellow (4) pixels until the next red(2) is hit or the end of row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        # find sequences of red pixels
        red_sequences = []
        in_sequence = False

        for c in range(cols):
          if output_grid[r,c] == 2:
            if in_sequence == False:
              red_sequences.append(c)
              in_sequence = True
          elif output_grid[r,c] != 2:
            in_sequence = False
        
        # fill the white spaces with yellow after the sequences of reds
        for seq_start in red_sequences:
          for c in range(seq_start+1, cols):
            if output_grid[r, c] == 0:
              output_grid[r, c] = 4
            elif output_grid[r,c] == 2:
              break

    return output_grid
```
