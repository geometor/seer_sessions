```python
"""
Identify contiguous regions of white pixels (0).
For each white region, determine if it touches the border of the grid.
If a white region does *not* touch the border:
  - Calculate its size (number of pixels).
  - If the size is 4 or less, fill the region with orange (7).
  - If the size is greater than 4, fill the region with azure (8).
Leave all gray pixels (5) and white regions that touch the border unchanged.
"""

import numpy as np
from collections import deque

def find_white_region(grid, start_row, start_col, visited, height, width):
    """
    Finds a connected white region starting from (start_row, start_col) using BFS.

    Args:
        grid (np.array): The input grid.
        start_row (int): Starting row index.
        start_col (int): Starting column index.
        visited (np.array): Boolean array tracking visited cells.
        height (int): Grid height.
        width (int): Grid width.

    Returns:
        tuple: (list_of_coords, touches_border)
               list_of_coords: A list of (row, col) tuples in the region.
               touches_border: Boolean, True if the region touches the grid border.
    """
    if visited[start_row, start_col] or grid[start_row, start_col] != 0:
        return [], False # Should not happen if called correctly, but safety check

    q = deque([(start_row, start_col)])
    region_coords = []
    visited[start_row, start_col] = True
    touches_border = False

    while q:
        r, c = q.popleft()
        region_coords.append((r, c))

        # Check if this pixel is on the border
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            touches_border = True

        # Explore neighbors (4-connectivity: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if it's white, and if not visited
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))

    return region_coords, touches_border


def transform(input_grid):
    """
    Fills enclosed white regions based on size: <=4 with orange (7), >4 with azure (8).
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid)
    height, width = grid.shape

    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # Keep track of visited white pixels to avoid processing regions multiple times
    visited = np.zeros_like(grid, dtype=bool)

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # If we find a white pixel (0) that hasn't been visited yet
            if grid[r, c] == 0 and not visited[r, c]:
                # Find the entire connected white region starting from this pixel
                region_coords, touches_border = find_white_region(grid, r, c, visited, height, width)

                # If the region is fully enclosed (doesn't touch the border)
                if not touches_border:
                    # Calculate the size of the region
                    region_size = len(region_coords)

                    # Determine the fill color based on size
                    fill_color = 7 if region_size <= 4 else 8 # orange for <= 4, azure for > 4

                    # Fill the region in the output grid
                    for reg_r, reg_c in region_coords:
                        output_grid[reg_r, reg_c] = fill_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```