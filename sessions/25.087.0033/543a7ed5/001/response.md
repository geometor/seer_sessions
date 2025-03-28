```python
import numpy as np
from collections import deque

"""
Identifies Magenta (6) shapes on an Azure (8) background.
Adds a Green (3) border (including diagonals) around each Magenta shape, replacing Azure pixels.
Identifies Azure regions completely enclosed by Magenta shapes (and potentially the new Green border).
Fills enclosed Azure regions with Yellow (4) if the region contains more than one pixel.
Single-pixel enclosed Azure regions remain Azure.
"""

def _is_valid(r, c, rows, cols):
    """Check if coordinates are within grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid):
    """
    Applies the border and fill transformation to the input grid.

    Args:
        input_grid (np.array): The input grid as a 2D numpy array.

    Returns:
        np.array: The transformed output grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = input_grid.copy()

    # --- Step 1: Add Green (3) border ---
    border_pixels = []
    for r in range(rows):
        for c in range(cols):
            # Only consider Azure pixels for potential bordering
            if input_grid[r, c] == 8:
                is_border = False
                # Check 8 neighbors (orthogonal and diagonal)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if _is_valid(nr, nc, rows, cols) and input_grid[nr, nc] == 6: # Magenta
                            is_border = True
                            break
                    if is_border:
                        break
                if is_border:
                    border_pixels.append((r, c))

    # Apply the green border to the output grid
    for r, c in border_pixels:
        output_grid[r, c] = 3 # Green

    # --- Step 2: Identify and fill enclosed holes ---

    # Create a grid to track visited pixels during reachability analysis
    visited_reachability = np.zeros_like(output_grid, dtype=bool)
    q_reachability = deque()

    # Start BFS from all boundary pixels that are Azure (8) or Green (3)
    for r in range(rows):
        for c in [0, cols - 1]:
            if not visited_reachability[r, c] and (output_grid[r, c] == 8 or output_grid[r, c] == 3):
                q_reachability.append((r, c))
                visited_reachability[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if not visited_reachability[r, c] and (output_grid[r, c] == 8 or output_grid[r, c] == 3):
                q_reachability.append((r, c))
                visited_reachability[r, c] = True

    # Perform BFS to find all Azure/Green pixels reachable from the boundary
    while q_reachability:
        r, c = q_reachability.popleft()
        # Check orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if _is_valid(nr, nc, rows, cols) and \
               not visited_reachability[nr, nc] and \
               (output_grid[nr, nc] == 8 or output_grid[nr, nc] == 3): # Azure or Green
                visited_reachability[nr, nc] = True
                q_reachability.append((nr, nc))

    # Create a grid to track visited pixels during hole identification
    visited_holes = np.zeros_like(output_grid, dtype=bool)

    # Iterate through the grid to find unvisited Azure pixels (potential holes)
    for r in range(rows):
        for c in range(cols):
            # If it's an Azure pixel and wasn't reached from the boundary
            if output_grid[r, c] == 8 and not visited_reachability[r, c] and not visited_holes[r, c]:
                # Found the start of a potential hole
                current_hole_pixels = []
                q_hole = deque([(r, c)])
                visited_holes[r, c] = True
                is_enclosed = True # Assume enclosed until proven otherwise (redundant check, but safe)

                # Perform BFS to find all connected Azure pixels in this hole
                while q_hole:
                    hr, hc = q_hole.popleft()
                    current_hole_pixels.append((hr, hc))

                    # Check orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nhr, nhc = hr + dr, hc + dc
                        if _is_valid(nhr, nhc, rows, cols):
                             # If neighbor is Azure and not visited for holes yet
                            if output_grid[nhr, nhc] == 8 and not visited_holes[nhr, nhc]:
                                visited_holes[nhr, nhc] = True
                                q_hole.append((nhr, nhc))
                            # Double-check if it touches a reachable area (shouldn't happen based on reachability BFS)
                            # elif visited_reachability[nhr, nhc] and (output_grid[nhr, nhc] == 8 or output_grid[nhr, nhc] == 3):
                            #     is_enclosed = False

                # After finding the whole component, check its size
                # We already know it's enclosed because it wasn't reached by the first BFS
                if len(current_hole_pixels) > 1:
                    # Fill the hole with Yellow (4)
                    for hr, hc in current_hole_pixels:
                        output_grid[hr, hc] = 4

    return output_grid.tolist() # Return as list of lists per standard

```