# dbc1a6ce • 020 • refine_coder

---
```python
"""
1.  **Identify Blue Pixel Groups:** Find all groups of connected blue pixels.  Two blue pixels are considered connected if they are cardinally adjacent (up, down, left, or right). A single, isolated blue pixel is also considered its own group.

2.  **Process Each Group:** For each identified blue pixel group:
    *   **If the group contains more than one blue pixel (connected = True):** Change all pixels within that group to azure (8).
    *   **If the group contains only a single blue pixel (connected = False):**
        * Change the single blue to azure
        * **Check for adjacent white (0) pixels:**  For each cardinally adjacent cell that is white (0), add an azure (8) pixel in that cell.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in the grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    return neighbors

def find_blue_groups(grid):
    """Finds all connected groups of blue pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    groups = []

    def dfs(row, col, current_group):
        """Depth-first search to find connected components."""
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != 1
        ):
            return
        visited[row, col] = True
        current_group.append((row, col))
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(row + dr, col + dc, current_group)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1 and not visited[r, c]:
                current_group = []
                dfs(r, c, current_group)
                groups.append(current_group)
    return groups

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all blue pixel groups
    blue_groups = find_blue_groups(input_grid)

    # Process each group
    for group in blue_groups:
        if len(group) > 1:
            # Connected group: Change all to azure
            for r, c in group:
                output_grid[r, c] = 8
        else:
            # Single pixel: change to azure and expand if needed.
            r, c = group[0]
            output_grid[r,c] = 8
            neighbors = get_neighbors(input_grid, r, c)
            for nr, nc in neighbors:
                if input_grid[nr, nc] == 0:  # Check for white adjacent pixels
                    output_grid[nr, nc] = 8
    return output_grid
```

