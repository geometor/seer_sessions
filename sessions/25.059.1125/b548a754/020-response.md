# b548a754 • 020 • refine_coder

---
```python
"""
1.  **Identify Seed Column:** The seed column is always the leftmost column (column 0).
2.  **Identify the Non-Black Region:** find the contiguous region of non-black
    pixels in the seed column.
3. **Determine Expansion Color**: The expansion color is always the color of
   the top pixel of the contiguous region.
4.  **Horizontal Expansion:** For each row containing the non-black region of
    the seed column, fill the grid with the `expansion_color` starting from column 0 up to, but not including, the last column.
5.  **Do Not Remove Isolated Pixels**: The rightmost column may contain an isolated pixel that should not be removed.
"""

import numpy as np

def find_seed_structure(grid):
    """Finds the seed structure and its properties."""
    rows, cols = grid.shape
    start_row = -1
    height = 0
    expansion_color = 0

    for r in range(rows):
        if grid[r, 0] != 0:
            if start_row == -1:
                start_row = r
                expansion_color = grid[r, 0]
            height += 1
        elif height > 0:
            break  # Stop once we find a gap

    return start_row, height, expansion_color

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the seed structure in the leftmost column
    start_row, height, expansion_color = find_seed_structure(input_grid)

    # Handle cases with no seed structure.
    if start_row == -1:
        return output_grid
    
    # Perform horizontal expansion up to the second to last column
    for r in range(start_row, min(start_row + height, rows)):
        for c in range(0, cols - 1):
            output_grid[r, c] = expansion_color
            
    return output_grid
```
