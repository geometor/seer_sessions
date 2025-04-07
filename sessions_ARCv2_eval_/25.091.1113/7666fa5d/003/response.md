```python
"""
This program transforms an input grid by filling enclosed regions of the background color (azure 8) with red (2).
1. It identifies the background color (azure 8).
2. It iterates through each pixel of the grid.
3. If a background pixel hasn't been visited yet, it initiates a flood fill (BFS) starting from that pixel.
4. During the flood fill, it collects all connected background pixels belonging to the same region and checks if any pixel in this region touches the grid's border.
5. If the flood fill completes and the region did *not* touch the border, all pixels identified in that region are colored red (2) in the output grid.
6. All pixels visited during any flood fill are marked to avoid redundant checks.
7. Non-background pixels and background pixels belonging to regions connected to the border remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Fills enclosed regions of the background color with red (2).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    grid = np.array(input_grid)
    output_grid = grid.copy()
    rows, cols = grid.shape
    
    # Define background and fill colors
    background_color = 8
    fill_color = 2
    
    # Create a boolean grid to mark visited pixels during any flood fill
    visited = np.zeros_like(grid, dtype=bool)

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # Start a flood fill only if the pixel is background and hasn't been visited
            if grid[r, c] == background_color and not visited[r, c]:
                
                # Store pixels of the current region being explored
                current_region_pixels = []
                # Flag to track if this region touches the border
                reached_border = False
                # Queue for BFS
                q = deque([(r, c)])
                
                # Mark the starting pixel as visited and add to the region list
                visited[r, c] = True
                current_region_pixels.append((r, c))

                # Perform BFS for the current connected background region
                while q:
                    curr_r, curr_c = q.popleft()

                    # Check if the current pixel is on the border
                    if curr_r == 0 or curr_r == rows - 1 or curr_c == 0 or curr_c == cols - 1:
                        reached_border = True # No need to break, continue exploring to mark all connected as visited

                    # Explore 4-way neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is background color and not yet visited
                            if grid[nr, nc] == background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                current_region_pixels.append((nr, nc))

                # After exploring the entire connected region:
                # If the region did not reach the border, fill it with the fill_color
                if not reached_border:
                    for pr, pc in current_region_pixels:
                        output_grid[pr, pc] = fill_color
                        
    return output_grid
```