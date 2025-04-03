```python
import numpy as np
from collections import deque

"""
Identify all contiguous blocks of the same non-zero color in the input grid.
Determine the block with the largest number of cells.
Create an output grid of the same dimensions as the input, initialized with zeros.
Fill the cells in the output grid corresponding to the largest block's coordinates with that block's color.
If there are no non-zero blocks or multiple blocks tie for the largest size, the behavior based on the examples implies a single largest block is always present and chosen.
"""

def _is_valid(r, c, rows, cols):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def _find_block(grid, start_row, start_col, visited):
    """
    Finds a contiguous block of a single color using Breadth-First Search (BFS).

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        visited (np.array): A boolean array tracking visited cells.

    Returns:
        tuple: (color, size, coordinates) of the found block,
               or (0, 0, []) if the start cell is zero or already visited.
    """
    rows, cols = grid.shape
    color = grid[start_row, start_col]

    # Ignore background color or already visited cells
    if color == 0 or visited[start_row, start_col]:
        return 0, 0, []

    block_coords = []
    q = deque([(start_row, start_col)])
    visited[start_row, start_col] = True
    block_size = 0

    while q:
        r, c = q.popleft()
        block_coords.append((r, c))
        block_size += 1

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if not visited, and if it has the same color
            if _is_valid(nr, nc, rows, cols) and \
               not visited[nr, nc] and \
               grid[nr, nc] == color:
                visited[nr, nc] = True
                q.append((nr, nc))

    return color, block_size, block_coords


def transform(input_grid):
    """
    Identifies the largest contiguous block of a single non-zero color
    and returns a grid containing only that block.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # Keep track of visited cells during block finding
    visited = np.zeros_like(grid, dtype=bool)

    # Store information about the largest block found so far
    largest_block_info = {'color': 0, 'size': 0, 'coords': []}

    # Iterate through each cell to find blocks
    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and hasn't been visited as part of another block
            if grid[r, c] != 0 and not visited[r, c]:
                # Find the complete block starting from this cell
                color, size, coords = _find_block(grid, r, c, visited)

                # Check if this block is larger than the current largest
                if size > largest_block_info['size']:
                    largest_block_info['color'] = color
                    largest_block_info['size'] = size
                    largest_block_info['coords'] = coords

    # Initialize the output grid with zeros (background color)
    output_grid = np.zeros_like(grid, dtype=int)

    # If a largest block was found (i.e., the input wasn't all zeros)
    if largest_block_info['size'] > 0:
        # Fill the output grid with the largest block
        for r_block, c_block in largest_block_info['coords']:
            output_grid[r_block, c_block] = largest_block_info['color']

    # Convert back to list of lists if necessary, otherwise return numpy array
    # Returning numpy array is generally fine and often preferred.
    # return output_grid.tolist()
    return output_grid
```