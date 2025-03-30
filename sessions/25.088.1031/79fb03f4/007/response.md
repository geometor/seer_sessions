```python
import numpy as np
from collections import deque

"""
Perform a flood fill originating from initial blue (1) pixels into adjacent white (0) areas, 
bounded by gray (5), azure (8) pixels, and grid boundaries. 
Initial blue, gray, and azure pixels remain unchanged. White pixels not reached by the fill
also remain unchanged.
"""

def transform(input_grid):
    """
    Applies a flood fill transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np) # Initialize output grid as a copy of input
    height, width = input_np.shape

    # Define colors
    white = 0
    blue = 1
    gray = 5
    azure = 8
    # Barrier colors (gray, azure) and fill color (blue) are implicitly handled by the logic
    # The fill only enters 'white' cells and stops otherwise.

    # Initialize queue for Breadth-First Search (BFS)
    queue = deque()

    # Find initial "seed" pixels for the flood fill
    # These are white pixels adjacent to initial blue pixels
    for r in range(height):
        for c in range(width):
            # Check only initial blue pixels as sources
            if input_np[r, c] == blue:
                # Check orthogonal neighbors
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc

                    # Check bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if neighbor is white in input AND still white in output (not yet processed/queued)
                        if input_np[nr, nc] == white and output_np[nr, nc] == white:
                            # Mark this seed pixel as blue in the output
                            output_np[nr, nc] = blue
                            # Add its coordinates to the queue to start the fill from here
                            queue.append((nr, nc))

    # Perform the flood fill using BFS
    while queue:
        # Get the next pixel to process
        r, c = queue.popleft()

        # Explore orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor was originally white AND is currently still white in the output grid
                # This means it's a fillable pixel that hasn't been reached yet.
                # We check input_np[nr, nc] == white because barriers (gray, azure) or initial blue 
                # should not be overwritten, even if the flood reaches them.
                if input_np[nr, nc] == white and output_np[nr, nc] == white:
                     # Change the neighbor's color to blue in the output grid
                    output_np[nr, nc] = blue
                    # Add the neighbor to the queue to continue the fill from there
                    queue.append((nr, nc))

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
```