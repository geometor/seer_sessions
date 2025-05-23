```python
"""
Transforms the input grid by identifying contiguous regions of white pixels (0). 
If a white region is fully enclosed (does not touch the grid border) AND 
is adjacent (8-way connectivity) to at least one initial blue pixel (1), 
then all pixels within that white region are changed to blue (1). 
All other pixels retain their original colors.
"""

import numpy as np
from collections import deque

def find_white_region_and_check_adjacency(start_r, start_c, input_grid, visited):
    """
    Performs a Breadth-First Search (BFS) to find a contiguous region of 
    white pixels (0) starting from (start_r, start_c). 
    It also determines if the region is enclosed within the grid boundaries 
    and if it is adjacent to any initial blue pixel (1).

    Args:
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        input_grid (np.ndarray): The original input grid.
        visited (np.ndarray): A boolean grid tracking visited white pixels.

    Returns:
        tuple: A tuple containing:
            - region_pixels (list): List of (row, col) tuples for the white region.
            - is_enclosed (bool): True if the region does not touch the border.
            - is_adjacent_to_blue (bool): True if the region is adjacent to an initial blue pixel.
    """
    height, width = input_grid.shape
    queue = deque([(start_r, start_c)])
    visited[start_r, start_c] = True
    
    region_pixels = []
    is_enclosed = True
    is_adjacent_to_blue = False
    
    # 8 directions for neighbors (horizontal, vertical, diagonal)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    while queue:
        r, c = queue.popleft()
        region_pixels.append((r, c))

        # Check if the current pixel is on the border
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            is_enclosed = False

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check adjacency to an initial blue pixel
                if input_grid[nr, nc] == 1:
                    is_adjacent_to_blue = True
                
                # Check if neighbor is white and not visited for BFS continuation
                elif input_grid[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))
            # Note: We don't need an else condition for out-of-bounds, 
            # as the boundary check itself contributes to the 'is_enclosed' logic.
            # Pixels with colors 2-9 act as natural boundaries for the BFS 
            # exploring white regions, but adjacency check still looks at them.

    return region_pixels, is_enclosed, is_adjacent_to_blue

def transform(input_grid):
    """
    Fills enclosed white regions adjacent to initial blue pixels with blue.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid.
    """
    height, width = input_grid.shape
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    # Keep track of visited white pixels to avoid processing the same region multiple times
    visited = np.zeros((height, width), dtype=bool)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # If we find a white pixel (0) that hasn't been visited yet
            if input_grid[r, c] == 0 and not visited[r, c]:
                # Find the entire contiguous white region it belongs to
                # and check its properties (enclosure, adjacency to blue)
                region_pixels, is_enclosed, is_adjacent_to_blue = find_white_region_and_check_adjacency(
                    r, c, input_grid, visited
                )

                # If the region is both enclosed and adjacent to an initial blue pixel
                if is_enclosed and is_adjacent_to_blue:
                    # Fill this region with blue (1) in the output grid
                    for pr, pc in region_pixels:
                        output_grid[pr, pc] = 1
                # Otherwise (not enclosed or not adjacent to blue), the region remains white
                # (no action needed as output_grid started as a copy).

    # Return the modified grid
    return output_grid
```