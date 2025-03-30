```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify the boundary color (Azure, 8) and the fill color (the single color present in the input grid that is neither White (0) nor Azure (8)).
2. Create a copy of the input grid to serve as the output grid.
3. Identify all White (0) pixels that are connected to the grid's outer border, either directly or through a path of other White (0) pixels. This can be done using a flood fill or Breadth-First Search (BFS) starting from all White (0) pixels on the border. Mark these reachable White (0) pixels.
4. Iterate through the grid. Any White (0) pixel that was *not* marked as reachable from the border in the previous step is considered 'enclosed' by the Azure (8) boundary.
5. Change the color of these enclosed White (0) pixels in the output grid to the identified fill color.
6. Leave all other pixels (Azure boundaries, original fill color pixels, and White pixels reachable from the border) unchanged.
7. Return the modified output grid.
"""

def transform(input_grid):
    """
    Fills enclosed white regions within azure boundaries using a specific 
    fill color found elsewhere in the grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # --- Identify boundary and fill colors ---
    boundary_color = 8 # Azure
    background_color = 0 # White
    
    # Find the unique fill color (not 0 or 8)
    unique_colors = np.unique(grid)
    fill_color = background_color # Default if no fill color found
    for color in unique_colors:
        if color != background_color and color != boundary_color:
            fill_color = color
            break
    
    # If no specific fill color is found besides white and azure, 
    # there's nothing to fill, return the original grid.
    # (Although examples suggest a fill color is always present)
    if fill_color == background_color:
        return output_grid.tolist()

    # --- Identify White (0) pixels reachable from the border ---
    visited = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Add all border White(0) pixels to the queue and mark visited
    for r in range(rows):
        if grid[r, 0] == background_color and not visited[r, 0]:
            queue.append((r, 0))
            visited[r, 0] = True
        if grid[r, cols - 1] == background_color and not visited[r, cols - 1]:
            queue.append((r, cols - 1))
            visited[r, cols - 1] = True
    for c in range(cols):
        if grid[0, c] == background_color and not visited[0, c]:
            queue.append((0, c))
            visited[0, c] = True
        if grid[rows - 1, c] == background_color and not visited[rows - 1, c]:
            queue.append((rows - 1, c))
            visited[rows - 1, c] = True

    # Perform BFS to find all reachable White(0) pixels
    while queue:
        r, c = queue.popleft()

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is White(0) and not visited
                if grid[nr, nc] == background_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # --- Fill enclosed White (0) regions ---
    # Iterate through the entire grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is White(0) and was *not* visited by the BFS, it's enclosed
            if grid[r, c] == background_color and not visited[r, c]:
                # Fill this pixel in the output grid with the fill color
                output_grid[r, c] = fill_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```