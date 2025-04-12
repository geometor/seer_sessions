```python
"""
Transformation Rule Hypothesis (Based on Standard Flood Fill):

1.  Create the output grid by making an exact copy of the input grid.
2.  Identify all pixels in the input grid that have the background color, white (0).
3.  From these white pixels, identify the subset located on the grid's boundary (top row, bottom row, left column, right column). These are the starting "source" pixels.
4.  Determine the set of all white pixels that can be reached starting from *any* source pixel by moving only between adjacent (up, down, left, right) white pixels. Let this set be the "fillable" pixels.
5.  Apply a selection rule (currently unknown) to choose a subset of the "fillable" pixels. These chosen pixels are the "target" pixels. 
    ***NOTE: This implementation assumes the simplest rule: all "fillable" pixels are "target" pixels. This assumption is known to be incorrect based on the provided training examples, as it leads to overfilling. The true selection rule remains unidentified.***
6.  Modify the output grid: For every pixel location `(r, c)` that belongs to the set of "target" pixels (in this implementation, all "fillable" pixels), change its color to yellow (4).
7.  Leave all other pixels in the output grid unchanged from their color in the input grid. This includes the original non-white shapes and any white pixels that were not "fillable".
"""

import copy
from collections import deque

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Fills the white areas (0) connected to the boundary with yellow (4),
    stopping at non-white pixels. Implements a standard flood fill from boundary.
    WARNING: This standard approach does not match the target outputs for training examples.
    """
    
    # 1. Create the output grid as an exact copy of the input grid.
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Define constants
    fill_color = 4
    background_color = 0

    # Initialize data structures for BFS (Flood Fill)
    queue = deque()
    
    # 2 & 3. Identify white (0) pixels on the boundary ("source" pixels)
    # Add them to the queue and immediately color them in the output grid
    # Marking them ensures they are processed and prevents re-adding corners.
    for r in range(height):
        for c in range(width):
            is_boundary = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
            if is_boundary and output_grid[r][c] == background_color:
                 # Mark as visited/filled and add to queue
                 output_grid[r][c] = fill_color
                 queue.append((r, c))

    # Define 4-way adjacent neighbors (dr, dc) for movement
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # 4. Determine all reachable ("fillable") white pixels via BFS
    while queue:
        r, c = queue.popleft() 

        # Explore neighbors
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc 

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is a background pixel (unvisited)
                # We check output_grid because visited pixels are already colored yellow
                if output_grid[nr][nc] == background_color:
                    # 6. (Implicitly via loop) Change color to fill color (mark as visited/target)
                    output_grid[nr][nc] = fill_color
                    # Add neighbor to the queue for further exploration
                    queue.append((nr, nc))

    # 7. Return the modified grid. Non-white pixels and unreachable white pixels
    # were never modified from the initial copy.
    return output_grid
```