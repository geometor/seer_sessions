```python
"""
Transforms a grid based on the following rules:
1.  Identifies Magenta (6) shapes on an Azure (8) background.
2.  Identifies connected regions of Azure (8) pixels that are fully enclosed by Magenta (6) pixels (using 8-way adjacency for checking enclosure) and do not touch the grid boundary.
3.  Fills enclosed Azure regions with Yellow (4) if the region contains more than one pixel. Single-pixel enclosed Azure regions remain Azure.
4.  Adds a Green (3) border (including diagonals, 8-way adjacency) around each Magenta shape by changing adjacent Azure pixels to Green.
5.  Crucially, if an Azure pixel qualifies for both becoming part of a Yellow fill (step 3) and a Green border (step 4), it becomes Yellow. Green borders only replace Azure pixels that are *not* part of a multi-pixel enclosed region.
"""

import numpy as np
from collections import deque

def _is_valid(r, c, rows, cols):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def _get_neighbors(r, c, rows, cols, connectivity=8):
    """Get valid neighbor coordinates."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            # Skip diagonal neighbors if connectivity is 4
            if connectivity == 4 and abs(dr) + abs(dc) > 1:
                continue
            nr, nc = r + dr, c + dc
            if _is_valid(nr, nc, rows, cols):
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Applies the enclosure filling and bordering transformation to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = input_np.copy() # Start with a copy

    # --- Step 1: Identify Azure pixels reachable from the boundary ---
    visited_reachable = np.zeros_like(input_np, dtype=bool)
    q_reachability = deque()

    # Add boundary Azure pixels to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if not visited_reachable[r, c] and input_np[r, c] == 8: # Azure
                q_reachability.append((r, c))
                visited_reachable[r, c] = True
    for c in range(1, cols - 1): # Avoid double-counting corners
        for r in [0, rows - 1]:
             if not visited_reachable[r, c] and input_np[r, c] == 8: # Azure
                q_reachability.append((r, c))
                visited_reachable[r, c] = True

    # Perform BFS to find all Azure pixels reachable from the boundary (using 8-way adjacency)
    while q_reachability:
        r, c = q_reachability.popleft()
        # Check 8 neighbors
        for nr, nc in _get_neighbors(r, c, rows, cols, connectivity=8):
            if not visited_reachable[nr, nc] and input_np[nr, nc] == 8: # Azure
                visited_reachable[nr, nc] = True
                q_reachability.append((nr, nc))

    # --- Step 2: Identify enclosed Azure regions and mark for Yellow fill ---
    visited_holes = np.zeros_like(input_np, dtype=bool)
    yellow_pixels = set()

    for r in range(rows):
        for c in range(cols):
            # If it's an Azure pixel, wasn't reached from boundary, and hasn't been visited for holes yet
            if input_np[r, c] == 8 and not visited_reachable[r, c] and not visited_holes[r, c]:
                # Found the start of a potential enclosed Azure component
                current_hole_pixels = []
                q_hole = deque([(r, c)])
                visited_holes[r, c] = True
                is_truly_enclosed = True # Check if all non-component neighbors are magenta - technically redundant because of boundary check, but good practice

                # BFS to find the full component (using 8-way adjacency)
                while q_hole:
                    hr, hc = q_hole.popleft()
                    current_hole_pixels.append((hr, hc))

                    for nhr, nhc in _get_neighbors(hr, hc, rows, cols, connectivity=8):
                        neighbor_val = input_np[nhr, nhc]
                        if neighbor_val == 8: # Azure
                            if not visited_reachable[nhr, nhc] and not visited_holes[nhr, nhc]:
                                visited_holes[nhr, nhc] = True
                                q_hole.append((nhr, nhc))
                        # Check for non-magenta neighbors (excluding other parts of the hole itself)
                        # This check ensures it's *only* surrounded by Magenta or itself.
                        # Since we already know it's not reachable from the boundary (which has Azure or is outside),
                        # any non-Magenta neighbor implies it's not truly enclosed by *only* Magenta.
                        # However, the boundary reachability check *should* cover this.
                        # elif neighbor_val != 6: # If neighbor is not Magenta and not part of the growing hole
                        #     # We need to be careful here. A neighbor might be part of the hole but not yet visited.
                        #     # The logic based on visited_reachable is sufficient.
                        #     pass


                # If the hole component has more than one pixel, mark it for yellow fill
                if len(current_hole_pixels) > 1:
                    for hr, hc in current_hole_pixels:
                        yellow_pixels.add((hr, hc))

    # --- Step 3: Identify potential Green border pixels ---
    potential_green_pixels = set()
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == 8: # Only Azure pixels can become Green
                is_border = False
                # Check 8 neighbors for Magenta
                for nr, nc in _get_neighbors(r, c, rows, cols, connectivity=8):
                    if input_np[nr, nc] == 6: # Magenta
                        is_border = True
                        break
                if is_border:
                    potential_green_pixels.add((r, c))

    # --- Step 4: Construct the final output grid ---
    # Apply Yellow fill first
    for r, c in yellow_pixels:
        output_grid[r, c] = 4 # Yellow

    # Apply Green border, only if the pixel wasn't turned Yellow
    for r, c in potential_green_pixels:
        if output_grid[r, c] == 8: # Check if it's still Azure
            output_grid[r, c] = 3 # Green

    # Magenta pixels remain unchanged (already copied from input_np)
    # Azure pixels that weren't filled or bordered remain Azure

    return output_grid.tolist()
```