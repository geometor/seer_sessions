```python
import numpy as np
from collections import deque

def find_regions(grid):
    """
    Identifies rectangular regions bordered by white (0) pixels.
    This function is not strictly necessary for the final flood fill approach 
    but could be useful for alternative strategies or more complex tasks.
    It's kept here for potential future reference but not used in the main transform.
    
    Returns: A list of tuples, each representing the inner bounds 
             (min_row, max_row, min_col, max_col) of a region.
             Bounds are inclusive for max_row/max_col.
    """
    # This function is complex to implement correctly for all edge cases
    # (e.g., touching rectangles, L-shaped white areas) and is not 
    # required for the identified flood-fill logic. A simpler approach 
    # is used in the main transform function.
    pass # Placeholder

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    Find all orange (7) pixels. For each orange pixel, perform a flood fill 
    operation outwards, changing adjacent gray (5) pixels to orange (7). 
    The flood fill stops when it encounters any pixel that is not gray (5), 
    including the white (0) borders often seen in the examples, or the grid boundaries.
    All other pixels retain their original color.
    """
    
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape
    
    # Colors
    ORANGE = 7
    GRAY = 5
    # WHITE = 0 # Implicitly a boundary for the fill

    # Queue for Breadth-First Search (BFS) based flood fill
    queue = deque()
    
    # Set to keep track of visited cells during the fill process for efficiency
    # We only need to track cells added to the queue to avoid redundant processing.
    visited = set()

    # Find initial orange pixels and add them to the queue and visited set
    for r in range(height):
        for c in range(width):
            if grid[r, c] == ORANGE:
                if (r, c) not in visited:
                     queue.append((r, c))
                     visited.add((r, c))
                # Note: The original orange pixels remain orange in the output_grid
                # because output_grid is initialized as a copy of grid.

    # Define 4-directional neighbors (up, down, left, right)
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    # Perform the flood fill using BFS
    while queue:
        curr_r, curr_c = queue.popleft()

        # Explore neighbors
        for i in range(4):
            nr, nc = curr_r + dr[i], curr_c + dc[i]

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is gray in the *original* grid
                # And check if it hasn't been visited/added to queue yet
                if grid[nr, nc] == GRAY and (nr, nc) not in visited:
                    # Change the color in the output grid to orange
                    output_grid[nr, nc] = ORANGE
                    # Mark as visited (added to queue)
                    visited.add((nr, nc))
                    # Add the neighbor to the queue to continue the fill
                    queue.append((nr, nc))

    return output_grid.tolist()
```