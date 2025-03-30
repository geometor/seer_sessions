import numpy as np
from collections import deque

"""
Transformation Rule:
1. Copy the input grid to create the output grid.
2. Identify Exterior White Pixels: Perform a flood fill (BFS) starting from all white (0) pixels on the grid borders. Mark all reachable white pixels as 'exterior'.
3. Initial Fill of Interior: Iterate through the grid. Change any white (0) pixel that was *not* marked as 'exterior' to azure (8). Keep track of the coordinates of these 'initially filled' azure pixels.
4. Identify Leak Points: Find all 'exterior' white pixels (identified in Step 2) that are orthogonally adjacent to any of the initially filled azure pixels (from Step 3). Collect the coordinates of all unique leak points.
5. Flood Fill from Leaks: Perform a second flood fill (BFS) starting simultaneously from *all* identified leak points. This flood fill propagates only into 'exterior' white pixels. Change the color of all reachable exterior white pixels during this flood fill to azure (8). The fill stops at grid boundaries, non-white pixels, or pixels already visited in this flood fill step.
6. Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a transformation involving filling enclosed areas and then
    flood-filling connected exterior areas from leak points.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_grid = input_array.copy() # Step 1: Copy input
    rows, cols = input_array.shape
    
    white = 0
    azure = 8

    # Helper to check if coordinates are within grid bounds
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # --- Step 2: Identify Exterior White Pixels using flood fill from borders ---
    is_exterior = np.zeros_like(input_array, dtype=bool)
    q_exterior = deque()

    # Add all border white cells to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if is_valid(r, c) and output_grid[r, c] == white and not is_exterior[r, c]:
                is_exterior[r, c] = True
                q_exterior.append((r, c))
    for c in range(cols):
        # Avoid adding corners twice
        if cols > 1:
            c_range = range(1, cols -1)
        else:
            c_range = range(cols)
            
        for r in [0, rows - 1]:
             if is_valid(r, c) and output_grid[r, c] == white and not is_exterior[r, c]:
                is_exterior[r, c] = True
                q_exterior.append((r, c))

    # Perform flood fill for exterior white cells
    while q_exterior:
        r, c = q_exterior.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and output_grid[nr, nc] == white and not is_exterior[nr, nc]:
                is_exterior[nr, nc] = True
                q_exterior.append((nr, nc))

    # --- Step 3: Fill enclosed white areas (those not exterior) with azure ---
    initial_fill_coords = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == white and not is_exterior[r, c]:
                output_grid[r, c] = azure
                initial_fill_coords.append((r, c))

    # --- Step 4: Identify Leak Points ---
    # Leak points are EXTERIOR WHITE cells adjacent to the INITIAL AZURE fill
    leak_points = set()
    for r_az, c_az in initial_fill_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_az + dr, c_az + dc # Coordinates of the neighbor
            # Check if neighbor is valid, IS exterior, and IS currently white
            if is_valid(nr, nc) and is_exterior[nr, nc] and output_grid[nr, nc] == white:
                 leak_points.add((nr, nc)) # Add the coordinate of the white neighbor

    # --- Step 5: Flood Fill from Leak Points into Exterior White Space ---
    q_leak_fill = deque()
    visited_in_leak_fill = set() # Tracks cells visited/queued in *this* BFS

    # Initialize the queue and visited set with the leak points
    # Also, color the initial leak points azure
    for r_leak, c_leak in leak_points:
        if (r_leak, c_leak) not in visited_in_leak_fill:
            output_grid[r_leak, c_leak] = azure
            visited_in_leak_fill.add((r_leak, c_leak))
            q_leak_fill.append((r_leak, c_leak))

    # Perform the flood fill starting from leak points
    while q_leak_fill:
        r, c = q_leak_fill.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Conditions to add neighbor to the leak fill:
            # 1. Must be valid coordinates
            # 2. Must be an EXTERIOR cell (identified in Step 2)
            # 3. Must currently be WHITE in the output grid
            # 4. Must not have been visited/queued in *this* leak fill BFS yet
            if (is_valid(nr, nc) and
                    is_exterior[nr, nc] and
                    output_grid[nr, nc] == white and
                    (nr, nc) not in visited_in_leak_fill):
                
                output_grid[nr, nc] = azure # Fill with azure
                visited_in_leak_fill.add((nr, nc)) # Mark as visited
                q_leak_fill.append((nr, nc)) # Add to queue for further expansion

    # --- Step 6: Return the final grid ---
    return output_grid.tolist()