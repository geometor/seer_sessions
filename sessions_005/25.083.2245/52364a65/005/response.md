```python
"""
1.  **Identify the Moving Edge:** Determine the edge (top, bottom, left, or right) where a contiguous block of non-azure pixels is adjacent to a contiguous block of azure (8) pixels. The "moving edge" is defined by the non-azure pixels.
2. **Determine Shift Direction:** The shift direction is perpendicular to the identified edge and towards the interior of the grid.  If the moving edge is the top edge, the shift direction is down. If the moving edge is the bottom edge, the shift is up.  If the moving edge is the left, the shift direction is right; and if it is right, the shift direction is left.
3.  **Shift the Pixels:** The non-azure pixels along the moving edge *shift* one position in the determined shift direction.
4.  **Fill with Azure:** The original positions of the shifted pixels are replaced with azure (8).
5. **Color Invariance:** The colors present in the output are the same as those present in the input, with the exception that new '8' pixels may appear.
"""

import numpy as np

def get_moving_edge(grid):
    """Identifies the moving edge and shift direction."""
    rows, cols = grid.shape
    
    # Check left edge
    if any(grid[r, 0] != 8 for r in range(rows)) and all(grid[r,1] == 8 for r in range(rows) if grid[r,0] != 8):
        return "left", "right"

    # Check right edge
    if any(grid[r, cols-1] != 8 for r in range(rows)) and all(grid[r,cols-2] == 8 for r in range(rows) if grid[r, cols-1] != 8):
        return "right", "left"

    # Check top edge
    if any(grid[0, c] != 8 for c in range(cols)) and all(grid[1,c] == 8 for c in range(cols) if grid[0,c] !=8):
        return "top", "down"

    # Check bottom edge
    if any(grid[rows-1, c] != 8 for c in range(cols)) and all(grid[rows-2,c] == 8 for c in range(cols) if grid[rows-1,c] != 8):
        return "bottom", "up"

    return None, None  # No moving edge found


def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify moving edge and shift direction
    edge, direction = get_moving_edge(input_grid)

    if edge is None:
        return output_grid # no transformation

    # Shift pixels and fill with azure
    if direction == "right":
        for r in range(rows):
            if output_grid[r, 0] != 8:
                output_grid[r, 1] = output_grid[r, 0]
                output_grid[r, 0] = 8
    elif direction == "left":
        for r in range(rows):
            if output_grid[r, cols-1] != 8:
                output_grid[r, cols-2] = output_grid[r, cols-1]
                output_grid[r, cols-1] = 8
    elif direction == "down":
        for c in range(cols):
            if output_grid[0, c] != 8:
                output_grid[1, c] = output_grid[0, c]
                output_grid[0, c] = 8
    elif direction == "up":
        for c in range(cols):
            if output_grid[rows-1, c] != 8:
                output_grid[rows-2, c] = output_grid[rows-1, c]
                output_grid[rows-1, c] = 8

    return output_grid
```