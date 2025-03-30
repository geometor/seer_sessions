```python
import numpy as np
from collections import deque

"""
Identifies all pixels that cannot reach the grid border via 4-directional 
movement without crossing an azure (8) pixel barrier. Any such unreachable 
pixel that is not itself azure is colored yellow (4) in the output grid. 
Azure pixels and pixels reachable from the border without crossing azure 
remain unchanged in the output.
"""

def transform(input_grid):
    """
    Fills background areas enclosed by azure pixels with yellow.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np) # Start with a copy of the input
    height, width = input_np.shape
    
    # Define colors used in the transformation
    BARRIER_COLOR = 8    # azure
    FILL_COLOR = 4       # yellow
    BACKGROUND_COLOR = 0 # white (implied, but useful for clarity)

    # 1. Initialize structures for Flood Fill (BFS)
    #    reachable_mask[r, c] will be True if (r, c) can be reached from the border
    #    without crossing a barrier.
    reachable_mask = np.zeros_like(input_np, dtype=bool)
    q = deque()

    # 2. Seed the queue with all border pixels that are NOT barriers.
    #    Mark these initial border pixels as reachable.
    for r in range(height):
        for c in range(width):
            # Check if the pixel is on any border
            is_border = (r == 0 or r == height - 1 or c == 0 or c == width - 1)
            if is_border:
                # If it's a non-barrier border pixel and not already added
                if input_np[r, c] != BARRIER_COLOR and not reachable_mask[r, c]:
                    reachable_mask[r, c] = True
                    q.append((r, c))

    # 3. Perform the Flood Fill (BFS) from the border pixels.
    while q:
        r, c = q.popleft()
        
        # Explore 4-directional neighbors (Up, Down, Left, Right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is not a barrier AND hasn't been reached yet
                if input_np[nr, nc] != BARRIER_COLOR and not reachable_mask[nr, nc]:
                    # Mark as reachable and add to the queue to explore from later
                    reachable_mask[nr, nc] = True
                    q.append((nr, nc))
                    
    # 4. Iterate through the entire grid after the flood fill is complete.
    for r in range(height):
        for c in range(width):
            # 5. Identify pixels that were NOT reached by the flood fill
            #    AND are not part of the barrier itself.
            #    These are the 'enclosed' non-barrier pixels.
            if not reachable_mask[r, c] and input_np[r, c] != BARRIER_COLOR:
                # 6. Change the color of these enclosed pixels in the output grid
                #    to the specified fill color.
                output_grid[r, c] = FILL_COLOR
                
    # 7. Pixels that were reachable, or were part of the barrier, remain
    #    unchanged in the output_grid because we started with a copy.

    # 8. Convert the final NumPy array back to a list of lists for the return value.
    return output_grid.tolist()
```