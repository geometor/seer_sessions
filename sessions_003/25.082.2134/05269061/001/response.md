```python
"""
1. **Identify the Input Sequence:** Extract the sequence of non-zero digits from the input grid, moving from top-left to bottom-right, and storing it in order.
2. **Reverse the Input Sequence** Create a reversed copy of the input sequence.
3. **Create the Output Grid:** Create a new 7x7 grid filled initially with zeros.
4.  **Interleave and Fill:**
    *   Iterate through rows of the new grid and perform one the following operations:
     1. set the row to elements starting from the head of the reversed sequence, repeating as necessary to fill the row.
     2.  set the row to elements starting from the head of the input sequence, repeating as necessary to fill the row.
    * Iterate between filling with each operation.
"""

import numpy as np

def extract_sequence(grid):
    """Extracts the sequence of non-zero digits from the grid."""
    sequence = []
    for row in grid:
        for cell in row:
            if cell != 0:
                sequence.append(cell)
    return sequence

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    # 1. Identify the Input Sequence
    input_sequence = extract_sequence(input_grid)

    # 2. Reverse the Input Sequence
    reversed_sequence = input_sequence[::-1]

    # 3. Create the Output Grid
    output_grid = np.zeros_like(input_grid)
    height, width = output_grid.shape

    # 4. Interleave and Fill
    for i in range(height):
        if i % 2 == 0:  # Even rows: use reversed sequence
            for j in range(width):
                output_grid[i, j] = reversed_sequence[j % len(reversed_sequence)]
        else:  # Odd rows: use original sequence
            for j in range(width):
                output_grid[i, j] = input_sequence[j % len(input_sequence)]

    return output_grid
```