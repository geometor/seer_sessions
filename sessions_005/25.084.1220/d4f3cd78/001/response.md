```python
import numpy as np
from collections import deque

# Color constants from ARC-AGI
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3
YELLOW = 4
GRAY = 5
MAGENTA = 6
ORANGE = 7
AZURE = 8
MAROON = 9

# Temporary marker for flood fill
TEMP_MARKER = -1 

def _is_valid(r, c, height, width):
    """Helper function to check if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def transform(input_grid):
    """
    Identifies a gray frame in the input grid. Fills the white area
    considered "inside" the frame with azure color (8). Identifies "gaps"
    in the gray frame - these are white pixels adjacent to both the gray
    frame and the newly filled azure interior. Finally, extends lines of
    azure color outwards from these gaps orthogonally towards the grid
    edges, stopping only at the grid boundary. The original gray frame
    pixels are preserved.
    """
    input_np = np.array(input_grid, dtype=int)
    # Create a working grid, initially a copy, that we can modify during processing
    working_grid = np.copy(input_np)
    height, width = input_np.shape

    # --- Step 1: Identify exterior white pixels using flood fill ---
    # Use Breadth-First Search (BFS) starting from all white border pixels.
    # Mark reachable white pixels with TEMP_MARKER in the working_grid.
    # This helps differentiate between white pixels outside the frame and inside.
    q = deque()
    
    # Initialize queue with all white border pixels and mark them
    for r in range(height):
        # Left and right borders
        for c in [0, width - 1]:
            if working_grid[r, c] == WHITE:
                working_grid[r, c] = TEMP_MARKER 
                q.append((r, c))
    # Top and bottom borders (excluding corners already added)
    for c in range(1, width - 1): 
        for r in [0, height - 1]:
            if working_grid[r, c] == WHITE:
                working_grid[r, c] = TEMP_MARKER
                q.append((r, c))

    # Perform BFS flood fill for exterior white pixels
    while q:
        r, c = q.popleft()
        # Explore orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds and is white (and hasn't been marked yet)
            if _is_valid(nr, nc, height, width) and working_grid[nr, nc] == WHITE:
                 working_grid[nr, nc] = TEMP_MARKER # Mark as exterior
                 