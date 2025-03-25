```python
"""
1.  **Identify Azure Block:** Locate the contiguous block of azure (8) pixels within the input grid.
2.  **Replace with Red:** Replace all pixels within the identified azure block with red (2) pixels.
3. **Preserve White:** Keep all other cells, which will be white (0) valued, unchanged.
4. **Output:** Generate the output grid reflecting these changes.
"""

import numpy as np

def find_contiguous_block(grid, color):
    # Find the first pixel of the specified color
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                start_row, start_col = r, c
                break
        else:
            continue
        break
    else:
        return []

    # Use a flood-fill approach to find all connected pixels of the same color
    visited = set()
    pixels = []
    queue = [(start_row, start_col)]

    while queue:
        r, c = queue.pop(0)
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            continue

        visited.add((r, c))
        pixels.append((r, c))

        # Add adjacent cells to the queue
        queue.append((r + 1, c))
        queue.append((r - 1, c))
        queue.append((r, c + 1))
        queue.append((r, c - 1))

    return pixels

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the contiguous block of azure (8) pixels
    azure_block = find_contiguous_block(input_grid, 8)

    # Replace azure pixels with red (2) pixels
    for r, c in azure_block:
        output_grid[r, c] = 2

    # make sure everything else is white (0)
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r,c] != 2:
                output_grid[r,c] = 0

    return output_grid
```