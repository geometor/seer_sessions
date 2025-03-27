"""
Identifies white (0) pixels enclosed by gray (5) pixels and performs a flood fill starting from these enclosed pixels, using azure (8) as the fill color.

1.  Identify all white (0) pixels reachable from the grid's border without crossing gray (5) pixels. This is done using a flood fill (BFS) starting from all border white pixels. Mark these reachable 'outside' pixels.
2.  Initialize the output grid as a copy of the input grid.
3.  Identify all white (0) pixels in the input grid that were *not* marked as 'outside' in step 1. These are the 'inside' pixels.
4.  Perform a second flood fill (BFS) on the output grid, starting simultaneously from all identified 'inside' white pixels.
5.  This second fill uses azure (8) as the fill color and spreads to adjacent (4-way) white (0) pixels.
6.  The fill stops at gray (5) pixels or grid boundaries.
7.  Return the final modified output grid.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill transformation based on enclosed white regions.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    rows, cols = input_grid.shape
    
    # Colors
    WHITE = 0
    GRAY = 5
    AZURE = 8
    
    # --- Step 1: Identify 'outside' white pixels ---
    
    # Use a boolean grid to mark visited/outside pixels
    is_outside = np.zeros_like(input_grid, dtype=bool) 
    q_outside = deque()

    # Add all border white pixels to the queue and mark them as outside
    for r in range(rows):
        for c in [0, cols - 1]:
            if input_grid[r, c] == WHITE and not is_outside[r, c]:
                is_outside[r, c] = True
                q_outside.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
            if input_grid[r, c] == WHITE and not is_outside[r, c]:
                is_outside[r, c] = True
                q_outside.append((r, c))

    # Perform BFS to find all reachable white pixels from the border
    while q_outside:
        r, c = q_outside.popleft()
        
        # Check 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is white and not yet marked as outside
                if input_grid[nr, nc] == WHITE and not is_outside[nr, nc]:
                    is_outside[nr, nc] = True
                    q_outside.append((nr, nc))

    # --- Step 2 & 3: Initialize output grid and identify 'inside' white pixels ---
    
    output_grid = np.copy(input_grid)
    q_fill = deque()
    
    # Iterate through the grid to find starting points for the fill
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white and NOT marked as outside, it's 'inside'
            if input_grid[r, c] == WHITE and not is_outside[r, c]:
                # Start the fill from here - change color immediately and add to queue
                if output_grid[r, c] == WHITE: # Check if not already filled (important for multiple starting points)
                    output_grid[r, c] = AZURE
                    q_fill.append((r, c))

    # --- Step 4, 5, 6: Perform the main flood fill with AZURE color ---
    
    while q_fill:
        r, c = q_fill.popleft()
        
        # Check 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is white (in the original sense) and not yet filled
                # Crucially, we check the original input_grid value (or output_grid before fill)
                # to allow filling through gaps, but only fill if the current output pixel is still WHITE
                if input_grid[nr, nc] == WHITE and output_grid[nr, nc] == WHITE:
                    output_grid[nr, nc] = AZURE
                    q_fill.append((nr, nc))
                    
    # --- Step 7: Return the result ---
    return output_grid