```python
"""
Transformation Rule Hypothesis: Selective Boundary Fill

1.  Create the initial output grid by making an exact copy of the input grid.
2.  Identify all white pixels (color 0) in the input grid.
3.  Determine the set of "source" pixels: white pixels located on the grid's boundary (top/bottom row or left/right column).
4.  Find the set of all "fillable" white pixels: these are all white pixels that can be reached starting from *any* source pixel by moving only between adjacent (up, down, left, right) white pixels. Use a standard reachability search (like flood fill or BFS) for this.
5.  Apply a specific, currently unknown, selection rule to choose a subset of the "fillable" pixels. These chosen pixels are the "target" pixels that will actually be colored yellow. 
    ***NOTE: This implementation assumes the simplest, incorrect rule: all "fillable" pixels are "target" pixels. This leads to overfilling compared to the expected outputs in the training examples. The correct selection rule remains unidentified.***
6.  Modify the output grid: For every pixel location `(r, c)` that belongs to the "target" pixel set (in this implementation, all "fillable" pixels), change its color to yellow (4).
7.  Leave all other pixels in the output grid unchanged from their original color in the input grid. This includes the original non-white shapes, any white pixels that were not "fillable", and any "fillable" white pixels that were not selected as "target" pixels by the (unknown) rule in step 5.
"""

import copy
from collections import deque

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Fills white areas (0) connected to the boundary with yellow (4),
    stopping at non-white pixels. Implements a standard flood fill from boundary.
    WARNING: This standard approach is known to NOT match the target outputs 
             for the provided training examples, as it doesn't incorporate the
             required (but unknown) selection rule for target pixels.
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
    # Add them to the queue and immediately color them in the output grid.
    # This serves as both initialization and marking these source pixels as visited/filled.
    for r in range(height):
        for c in range(width):
            is_boundary = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
            # Check if it's a white pixel on the boundary AND hasn't been processed yet
            # (Checking output_grid ensures corners aren't added twice)
            if is_boundary and output_grid[r][c] == background_color:
                 # Mark as visited/filled (color it yellow) and add to queue
                 output_grid[r][c] = fill_color
                 queue.append((r, c))

    # Define 4-way adjacent neighbors (dr, dc) for movement
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # 4. Determine all reachable ("fillable") white pixels via BFS
    #    and implicitly perform steps 5 & 6 assuming target=fillable.
    while queue:
        r, c = queue.popleft() # Get the next pixel to process

        # Explore its neighbors
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc # Calculate neighbor coordinates

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is a background pixel (unvisited)
                # We check the output_grid because visited pixels have already been colored yellow
                if output_grid[nr][nc] == background_color:
                    # 5 & 6. Mark as visited/target by changing color to fill color
                    output_grid[nr][nc] = fill_color
                    # Add neighbor to the queue for further exploration
                    queue.append((nr, nc))

    # 7. Return the modified grid. Pixels not visited by the BFS
    #    (original non-white shapes, unreachable white pixels, and 
    #     potentially fillable-but-not-targeted pixels if the rule were known)
    #    retain their initial color from the input grid copy.
    return output_grid
```