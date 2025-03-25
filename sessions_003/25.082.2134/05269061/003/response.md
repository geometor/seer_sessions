```python
"""
1. **Extract Input Sequence:** Scan the input grid from top-left to bottom-right, row by row. Create a list containing all non-zero digits encountered, preserving their order.
2. **Reverse the Sequence:** Create a reversed copy of the extracted sequence.
3. **Create Output Grid:** Create an output grid of the same dimensions as the input grid, initially filled with zeros (or any default value).
4. **Fill Output Grid:** Iterate through each row of the output grid. For *every* row, fill the row by repeating the reversed sequence. The index into the reversed sequence should wrap around (using the modulo operator) so that if the sequence is shorter than the row length, it repeats seamlessly.
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
    # 1. Extract Input Sequence
    input_sequence = extract_sequence(input_grid)

    # 2. Reverse the Sequence
    reversed_sequence = input_sequence[::-1]

    # 3. Create Output Grid
    output_grid = np.zeros_like(input_grid)
    height, width = output_grid.shape

    # 4. Fill Output Grid
    for i in range(height):
        for j in range(width):
            output_grid[i, j] = reversed_sequence[j % len(reversed_sequence)]

    return output_grid
```