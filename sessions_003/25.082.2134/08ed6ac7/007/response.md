```python
"""
Replaces each contiguous block of '5's in the input grid with a unique sequence
of numbers, starting from 1.  Contiguous blocks are defined by 4-way
connectivity (up, down, left, right). The sequence increments for each
separate contiguous block, and the replacement is done in-place.
"""

import numpy as np

def get_contiguous_blocks(grid, value):
    """
    Finds contiguous blocks of a given value in the grid.
    Returns a list of lists of (row, col) tuples, each representing a block.
    Prioritizes top-left blocks.
    """
    blocks = []
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == value and not visited[r, c]:
                block = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    curr_r, curr_c = stack.pop()
                    block.append((curr_r, curr_c))

                    # Check adjacent cells (4-way connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if 0 <= new_r < grid.shape[0] and 0 <= new_c < grid.shape[1] and \
                           grid[new_r, new_c] == value and not visited[new_r, new_c]:
                            stack.append((new_r, new_c))
                            visited[new_r, new_c] = True
                blocks.append(block)

    return blocks

def transform(input_grid):
    """
    Transforms the input grid by replacing each contiguous block of 5s with
    a unique sequence of numbers.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    output_grid = np.copy(input_grid)
    replacement_sequence = 1

    # Find all contiguous blocks of '5's.
    blocks = get_contiguous_blocks(output_grid, 5)

    # Iterate through each block and replace its pixels with the sequence.
    for block in blocks:
        for r, c in block:
            output_grid[r, c] = replacement_sequence
        replacement_sequence += 1

    return output_grid
```