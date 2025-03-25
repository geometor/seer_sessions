```python
"""
1.  **Divide and Conquer:** Divide the input 30x30 grid into non-overlapping 3x3 blocks.
2.  **Block Analysis, and Selection:** For each 3x3 block in the input grid, find the cell with the most occurrences within the 3x3 block.
3.  **Output Construction, and Placement:** Output the most frequent number in each block. Output is in top-to-bottom, left-to-right order, where top-to-bottom is the major order, and left-to-right is the minor order.
"""

import numpy as np
from collections import Counter

def get_most_frequent_color(block):
    """Finds the most frequent color in a block, excluding 1s."""
    counts = Counter(block.flatten())
    # Remove 1 from consideration if it exists
    if 1 in counts:
        del counts[1]
    if not counts:  # Handle the case where the block only contains 1s
        return 1
    most_common = counts.most_common(1)
    return most_common[0][0]


def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = rows // 3
    output_cols = cols // 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through 3x3 blocks
    for i in range(0, rows, 3):
        for j in range(0, cols, 3):
            block = input_grid[i:i+3, j:j+3]
            # find most frequent color
            most_frequent = get_most_frequent_color(block)
            # output the most frequent into output grid
            output_grid[i//3, j//3] = most_frequent

    return output_grid.tolist()
```