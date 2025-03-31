```python
"""
Transformation Rule Natural Language Description:

The transformation identifies regions enclosed by azure (8) pixels. 
First, it determines which white (0) pixels are 'inside' these regions by performing a flood fill from the grid borders; any white pixel *not* reached by this initial fill is considered 'inside'.
Then, within each enclosed region ('inside' area), it performs a separate flood fill operation starting from any existing red (2) pixels found within that specific 'inside' area. 
The fill color is red (2), and it propagates cardinally (up, down, left, right) only to adjacent 'inside' white (0) pixels. 
The fill is constrained by the azure (8) boundaries and does not spread to 'outside' white pixels or other non-white pixels. Pixels outside the azure boundaries and 'inside' white pixels not reachable from a red seed remain unchanged. Azure (8) pixels themselves remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Performs a constrained flood fill with red (2) starting from existing red pixels,
    limited to white (0) pixels located inside regions bounded by azure (8) pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify 'inside' white pixels
    # Initialize a boolean grid to track if a white pixel is inside (True) or outside (False)
    # Initially assume all are potentially inside, except non-white pixels.
    is_inside = (input_grid == 0)
    outside_queue = deque()

    # Add all border white pixels to the queue and mark them as outside
    for r in range(rows):
        for c in [0, cols - 1]: # Left and right borders
            if is_inside[r, c]:
                is_inside[r, c] = False
                outside_queue.append((r, c))
        # Avoid double-adding corners
        if r == 0 or r == rows - 1:
            for c in range(1, cols - 1): # Top and bottom borders (excluding corners)
                 if is_inside[r, c]:
                    is_inside[r, c] = False
                    outside_queue.append((r, c))

    # Perform BFS to find all white pixels reachable from the outside
    while outside_queue:
        r, c = outside_queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds and if the neighbor is white and still marked as 'inside'
            if 0 <= nr < rows and 0 <= nc < cols and is_inside[nr, nc]:
                is_inside[nr, nc] = False # Mark as outside
                outside_queue.append((nr, nc))

    # 2. Perform constrained red flood fill
    red_fill_queue = deque()
    visited_red_fill = set() # Keep track of visited cells for *this* fill

    # Seed the queue with initial red pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                # Only add valid starting points (should inherently be inside, but good practice)
                if 0 <= r < rows and 0 <= c < cols: # Basic bounds check
                   red_fill_queue.append((r,c))
                   visited_red_fill.add((r,c))
                   # No need to change output_grid color here, it's already red

    # Perform BFS for the red fill, constrained to 'inside' white pixels
    while red_fill_queue:
        r, c = red_fill_queue.popleft()

        # Explore cardinal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check conditions for filling the neighbor:
            # 1. Within grid bounds
            # 2. Not already visited in *this* red fill
            # 3. Is an 'inside' white pixel (input was 0 and is_inside is True)
            if (0 <= nr < rows and 0 <= nc < cols and
                    (nr, nc) not in visited_red_fill and
                    input_grid[nr, nc] == 0 and
                    is_inside[nr, nc]):

                # Conditions met: fill the pixel
                output_grid[nr, nc] = 2
                visited_red_fill.add((nr, nc))
                red_fill_queue.append((nr, nc))

    # Return the modified grid
    return output_grid
```