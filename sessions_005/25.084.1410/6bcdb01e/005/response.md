```python
"""
Identifies distinct regions enclosed by azure (8) pixels and grid boundaries using 4-way connectivity.
For each region, determines if it contains any initial green (3) pixels.
If a region contains at least one initial green pixel, all orange (7) pixels 
within that specific region are converted to green (3) in the output grid.
Pixels in regions without any initial green pixels, azure pixels, and other
non-orange pixels within source-containing regions remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a region-based color transformation based on 4-way connectivity.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    np_input = np.array(input_grid, dtype=int)
    output_grid = np_input.copy() # Initialize output grid as a copy of the input
    height, width = np_input.shape

    # Define colors
    GREEN = 3
    ORANGE = 7
    AZURE = 8

    # Keep track of visited cells during region identification
    visited = np.zeros_like(np_input, dtype=bool)
    regions = [] # Store info about each region: [{'coords': set(), 'has_green': bool}]

    # Define 4 directions for neighbor checking (horizontal and vertical connectivity)
    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    # 1. Identify all distinct contiguous regions of non-azure pixels using 4-way BFS
    for r in range(height):
        for c in range(width):
            # If this cell is not azure and hasn't been visited yet, start a new region search (BFS)
            if np_input[r, c] != AZURE and not visited[r, c]:
                current_region_coords = set()
                current_region_has_green = False
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_region_coords.add((row, col))

                    # Check if this cell in the original input grid is green
                    if np_input[row, col] == GREEN:
                        current_region_has_green = True

                    # Explore neighbors using 4-way connectivity
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc

                        # Check bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # If neighbor is not azure and not visited
                            if np_input[nr, nc] != AZURE and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store the found region and whether it contained any green pixels
                regions.append({
                    'coords': current_region_coords,
                    'has_green': current_region_has_green
                })

    # 2. Transform orange pixels to green only in regions that initially contained green
    for region_info in regions:
        # Check if this specific region contained at least one green pixel
        if region_info['has_green']:
            # Iterate through all coordinates within this region
            for r, c in region_info['coords']:
                # If the pixel in the *input* grid at this coordinate was orange
                if np_input[r, c] == ORANGE:
                    # Change the corresponding pixel in the *output* grid to green
                    output_grid[r, c] = GREEN
        # Pixels in regions without initial green remain unchanged (already copied)
        # Azure pixels remain unchanged (already copied)
        # Non-orange pixels within green-containing regions remain unchanged (already copied)


    # Convert the final numpy array back to a list of lists for the required output format
    return output_grid.tolist()
```