# 8e5a5113 • 012 • refine_coder

---
```python
"""
The core transformation involves identifying a repeating color sequence *within each row* of the input grid and extending that pattern across the entire row, replacing any '0' (white) pixels. If a row contains only '0' pixels, it will still be only '0's.
In cases where there are distinct row patterns, the pattern is shifted to start from the beginning of the row, and '0's may be added to end.

1.  **Iterate through each row** of the input grid.
2.  **Identify the repeating color sequence** : within the row find non-zero colors, up to the first zero after non-zeros start.
3.  **Extend/Repeat Pattern**: Repeat the identified sequence across the entire row to the right, starting from the beginning of the sequence.
4. If the row has a distinct pattern, shift the whole pattern so it starts from the left and fill any remaining cells with '0' if needed.
"""

import numpy as np

def find_repeating_sequence(row):
    """Finds the repeating non-zero sequence in a row."""
    sequence = []
    started = False
    for val in row:
        if val != 0:
            started = True
            sequence.append(val)
        elif started:
            break
    return sequence

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Find the repeating sequence in the current row
        sequence = find_repeating_sequence(input_grid[r])

        #if we have a sequence
        if (len(sequence) > 0):
          # Extend the pattern across the entire row
          for c_fill in range(cols):
            output_grid[r, c_fill] = sequence[c_fill % len(sequence)]
        #else, consider row pattern shifting if sequence is empty, but not a zero row
        elif any(input_grid[r] != 0): #distinct row
            # find the pattern
            pattern = []
            for c in range(cols):
                if input_grid[r,c]!=0:
                    pattern.append(input_grid[r,c])
            #shift the pattern so it fills the cells, then fill the remaining cells with 0
            for c in range(cols):
                if c < len(pattern):
                    output_grid[r,c] = pattern[c]
                else:
                    output_grid[r,c] = 0

    return output_grid
```
