```python
import numpy as np
from collections import deque

"""
Identifies all distinct contiguous objects composed solely of yellow (4) pixels in the input grid, considering 8-way adjacency (horizontal, vertical, diagonal). 
If a yellow object consists of exactly one pixel, that pixel's color is changed to white (0) in the output grid. 
All other pixels retain their original colors.
"""

def find_connected_object(grid, start_row, start_col, target_color, visited):
    """
    Finds all connected pixels of a target_color starting from (start_row, start_col)
    using Breadth-First Search (BFS) considering 8-way adjacency.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        target_color (int): The color of the object to find.
        visited (np.array): A boolean grid of the same shape as grid,
                             marking visited pixels.

    Returns:
        list: A list of (row, col) tuples representing the pixels in the object.
              Returns an empty list if the starting pixel is not the target color
              or has already been visited.
    """
    rows, cols = grid.shape
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       visited[start_row, start_col] or \
       grid[start_row, start_col] != target_color:
        return []

    object_pixels = []
    queue = deque([(start_row, start_col)])
    visited[start_row, start_col] = True

    while queue:
        r, c = queue.popleft()
        object_pixels.append((r, c))

        # Check 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip self

                nr, nc = r + dr, c + dc

                # Check bounds, color, and visited status
                if 0 <= nr < rows and 0 <= nc < cols and \
                   not visited[nr, nc] and \
                   grid[nr, nc] == target_color:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    return object_pixels


def transform(input_grid):
    """
    Transforms the input grid by changing single-pixel yellow (4) objects to white (0).

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # Initialize output grid as a copy of the input
    output_grid_np = np.copy(input_grid_np)

    # Keep track of visited pixels to avoid processing the same object multiple times
    visited = np.zeros_like(input_grid_np, dtype=bool)

    target_color = 4  # Yellow
    replacement_color = 0 # White

    # Iterate through each pixel of the grid
    for r in range(rows):
        for c in range(cols):
            # If the pixel is the target color and hasn't been visited yet
            if input_grid_np[r, c] == target_color and not visited[r, c]:
                # Find the complete connected object starting from this pixel
                object_pixels = find_connected_object(input_grid_np, r, c, target_color, visited)

                # Check if the object size is exactly 1
                if len(object_pixels) == 1:
                    # The object contains only the starting pixel (r, c)
                    # Change the color of this pixel in the output grid
                    output_grid_np[r, c] = replacement_color

    # Convert the result back to a list of lists
    return output_grid_np.tolist()

```