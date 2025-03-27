"""
Identifies white (0) pixels enclosed by gray (5) pixels and performs a flood fill starting from these enclosed pixels, using azure (8) as the fill color. The fill expands to adjacent white pixels and stops only at gray pixels or grid boundaries.

1. Initialize the output grid as a copy of the input grid.
2. Identify 'outside' non-gray pixels: Perform a BFS starting from all non-gray border pixels. Mark all reachable non-gray pixels as 'visited'. Gray pixels act as barriers.
3. Identify 'seed' pixels: Iterate through the input grid. Any white pixel (0) that was *not* marked as 'visited' in the previous step is a seed pixel for the fill.
4. Initialize a second BFS queue (`q_fill`) and add all identified seed pixels to it. Immediately change the color of these seed pixels in the output grid to azure (8).
5. Perform the fill BFS: While `q_fill` is not empty, dequeue a pixel (r, c). For each 4-way neighbor (nr, nc):
    a. Check if the neighbor is within bounds.
    b. Check if the neighbor was originally white (`input_grid[nr, nc] == WHITE`).
    c. Check if the neighbor is currently white in the output grid (`output_grid[nr, nc] == WHITE`), meaning it hasn't been filled yet.
    d. If all conditions are met, change the neighbor's color in the output grid to azure (8) and enqueue it.
6. Return the final modified output grid.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill transformation starting from enclosed white regions.

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
    
    # --- Step 1: Initialize output grid ---
    output_grid = np.copy(input_grid)

    # --- Step 2: Identify 'outside' non-gray pixels ---
    
    # Use a boolean grid to mark visited pixels during the border BFS
    visited_from_border = np.zeros_like(input_grid, dtype=bool) 
    q_border = deque()

    # Add all border non-gray pixels to the queue and mark them as visited
    for r in range(rows):
        for c in [0, cols - 1]:
            if input_grid[r, c] != GRAY and not visited_from_border[r, c]:
                visited_from_border[r, c] = True
                q_border.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
            # Avoid adding corners twice
            if input_grid[r, c] != GRAY and not visited_from_border[r, c]:
                visited_from_border[r, c] = True
                q_border.append((r, c))

    # Perform BFS from border non-gray pixels
    while q_border:
        r, c = q_border.popleft()
        
        # Check 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is not gray and not yet visited
                if input_grid[nr, nc] != GRAY and not visited_from_border[nr, nc]:
                    visited_from_border[nr, nc] = True
                    q_border.append((nr, nc))

    # --- Step 3 & 4: Identify 'seed' pixels and initialize the fill BFS ---
    
    q_fill = deque()
    seeds_found = False # Flag to check if any seeds were identified
    
    # Iterate through the grid to find starting points (seeds) for the fill
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white and NOT reachable from the border (not visited), it's a seed
            if input_grid[r, c] == WHITE and not visited_from_border[r, c]:
                # Check if it's not already filled (relevant if seeds overlap, though unlikely here)
                if output_grid[r, c] == WHITE: 
                    output_grid[r, c] = AZURE
                    q_fill.append((r, c))
                    seeds_found = True

    # Optimization: If no seeds were found, the output is same as input
    # This handles cases where there are no enclosed areas.
    if not seeds_found:
        return output_grid # Return the original copy

    # --- Step 5: Perform the main flood fill with AZURE color ---
    
    while q_fill:
        r, c = q_fill.popleft()
        
        # Check 4-way neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds (Condition i)
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor was originally white (Condition ii)
                # AND check if neighbor is currently white in output (Condition iii)
                if input_grid[nr, nc] == WHITE and output_grid[nr, nc] == WHITE:
                    # Fill with azure and enqueue (Condition iv)
                    output_grid[nr, nc] = AZURE
                    q_fill.append((nr, nc))
                    
    # --- Step 6: Return the result ---
    return output_grid