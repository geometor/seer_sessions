"""
1.  **Background Transformation:** Change all pixels with a value of 0 (black) in the input grid to a value of 3 (green) in the output grid.
2.  **Identify Blue Boundary:** Identify all pixels with a value of 1 (blue) in the input grid that form a connected component.  This connected component defines the "boundary." It does *not* need to be closed.
3.  **Boundary Color Change:** Change the color of all pixels identified as part of the blue boundary in step 2 to 2 (red) in the output grid.
4.  **Preserve all other pixels:** All pixels that were not 0 (black) and are not part of the identified boundary, remain unchanged in the output grid.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Change Background
    output_grid[output_grid == 0] = 3

    # Helper function to find connected components of a given color
    def get_connected_components(grid, color):
        visited = set()
        components = []

        def bfs(r, c):
            queue = deque([(r, c)])
            component = []
            while queue:
                row, col = queue.popleft()
                if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
                    continue
                visited.add((row, col))
                component.append((row, col))
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    queue.append((row + dr, col + dc))
            return component

        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r, c] == color and (r, c) not in visited:
                    components.append(bfs(r, c))
        return components

    # 2. Identify Blue Boundary (all blue connected components)
    blue_components = get_connected_components(input_grid, 1)

    # 3. Boundary Color Change
    for component in blue_components:
        for r, c in component:
            output_grid[r, c] = 2

    # 4. Preserve other pixels (implicit in steps 1 and 3)
    return output_grid