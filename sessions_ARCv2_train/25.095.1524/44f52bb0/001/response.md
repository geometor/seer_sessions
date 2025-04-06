```python
import numpy as np

def transform(input_grid: list[list[int]]) -> int:
    """
    Examines a 3x3 input grid containing 0s and 2s.
    Outputs 7 if any two '2's are directly adjacent (horizontally or vertically).
    Outputs 1 if no two '2's are adjacent.
    """

    # Get grid dimensions (assuming 3x3, but good practice)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell contains a '2'
            if input_grid[r][c] == 2:
                # Define potential neighbors (up, down, left, right)
                neighbors = [
                    (r - 1, c),  # Up
                    (r + 1, c),  # Down
                    (r, c - 1),  # Left
                    (r, c + 1)   # Right
                ]

                # Check each neighbor
                for nr, nc in neighbors:
                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor also contains a '2'
                        if input_grid[nr][nc] == 2:
                            # If an adjacent '2' is found, return 7 immediately
                            return 7

    # If the loops complete without finding adjacent '2's, return 1
    return 1
```