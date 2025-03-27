"""
Identifies distinct regions enclosed by azure (8) pixels and grid boundaries. 
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
    Applies a region-based color transformation.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    np_input = np.array(input_grid, dtype=int)
    output_grid = np_input.copy()
    height, width = np_input.shape

    # Define colors
    GREEN = 3
    ORANGE = 7
    AZURE = 8

    # Keep track of visited cells during region identification
    visited = np.zeros_like(np_input, dtype=bool)
    regions = [] # Store info about each region: [{'coords': set(), 'has_green': bool}]

    # Define 8 directions for neighbor checking (connectivity)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # 1. Identify all distinct contiguous regions of non-azure pixels
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

                    # Check if this cell is initially green
                    if np_input[row, col] == GREEN:
                        current_region_has_green = True

                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc

                        # Check bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # If neighbor is not azure and not visited
                            if np_input[nr, nc] != AZURE and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store the found region and its green status
                regions.append({
                    'coords': current_region_coords,
                    'has_green': current_region_has_green
                })

    # 2. Transform orange pixels to green only in regions that initially contained green
    for region_info in regions:
        if region_info['has_green']:
            for r, c in region_info['coords']:
                # If the pixel in the *input* grid was orange
                if np_input[r, c] == ORANGE:
                    # Change it to green in the *output* grid
                    output_grid[r, c] = GREEN

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()