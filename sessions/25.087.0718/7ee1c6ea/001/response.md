```python
"""
Identifies a region enclosed by gray (5) pixels. Within this enclosed region,
finds the two dominant non-gray (5) and non-white (0) colors present.
Swaps the positions of pixels having these two identified colors only within
the enclosed region. All other pixels (gray frame, pixels outside the frame,
and white pixels inside the frame) remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid by swapping two specific colors within a gray-enclosed region.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # --- 1. Identify pixels reachable from the border (outside or frame) ---
    visited = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add border cells to queue if not gray (5)
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] != 5 and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
            if grid[r, c] != 5 and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))

    # Perform flood fill from the border cells
    while q:
        r, c = q.popleft()
        # Check neighbors (4-connectivity: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If neighbor is not gray, not visited, add to queue
                if grid[nr, nc] != 5 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # --- 2. Identify interior pixels and their colors ---
    interior_pixels = []
    interior_colors = set()
    for r in range(rows):
        for c in range(cols):
            # Interior pixels are those not visited by flood fill and not part of the gray frame
            if not visited[r, c] and grid[r, c] != 5:
                interior_pixels.append((r, c))
                interior_colors.add(grid[r, c])

    # --- 3. Identify the two colors to swap ---
    # Filter out gray (5) and white (0)
    swap_colors = [color for color in interior_colors if color != 5 and color != 0]

    # Ensure exactly two swap colors were found (as per observed examples)
    if len(swap_colors) != 2:
        # If not exactly two, return the original grid or handle error
        # For this task, based on examples, we assume exactly two will be found.
        # If zero or one found, no swap happens. If >2, this logic might be incomplete.
        # Let's proceed assuming 2 colors are found based on the training data.
        # If len == 0 or 1, the loop below simply won't perform any swaps.
        pass

    if len(swap_colors) == 2:
      color_a = swap_colors[0]
      color_b = swap_colors[1]

      # --- 4. Perform the swap within the interior region ---
      for r, c in interior_pixels:
          if grid[r, c] == color_a:
              output_grid[r, c] = color_b
          elif grid[r, c] == color_b:
              output_grid[r, c] = color_a
          # Pixels with other colors (like 0) within the interior remain unchanged

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```