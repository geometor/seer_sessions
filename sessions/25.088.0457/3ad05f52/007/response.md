```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Initialization:** Create a copy of the input grid, which will become the output grid.
2.  **Identify Boundary and Background:** Define the boundary color as Azure (8) and the background color as White (0).
3.  **Identify External White Region:**
    a. Perform a Breadth-First Search (BFS) starting from all White (0) pixels located on the absolute border (edges) of the grid.
    b. Mark all reachable White (0) pixels during this BFS as 'external'.
4.  **Identify and Process Internal Regions:**
    a. Initialize a 'visited' tracker (e.g., a boolean grid) to keep track of pixels already processed or part of the boundary/external region. Mark all Azure (8) pixels and all identified 'external' White (0) pixels as initially visited.
    b. Iterate through every pixel (r, c) of the grid.
    c. If the pixel (r, c) has *not* been visited:
        i.  Start a new BFS/region discovery from this pixel. This signifies the beginning of a distinct internal region.
        ii. Initialize an empty list `current_region_pixels` to store the coordinates of all pixels belonging to this region.
        iii. Initialize `region_fill_color` to `None`. This variable will store the non-White, non-Azure color found within the region, if any.
        iv. Add the starting pixel (r, c) to the BFS queue, mark it as visited, and add it to `current_region_pixels`. Check its color and update `region_fill_color` if it's a potential fill color.
        v.  While the BFS queue for this region is not empty:
            *   Dequeue a pixel `(curr_r, curr_c)`.
            *   Explore its orthogonal neighbors `(nr, nc)`.
            *   For each valid neighbor (within bounds, not boundary color 8, and not visited):
                *   Mark the neighbor as visited.
                *   Enqueue the neighbor.
                *   Add the neighbor's coordinates `(nr, nc)` to `current_region_pixels`.
                *   Check the neighbor's color in the *input* grid. If it's neither White (0) nor Azure (8), set `region_fill_color` to this color. (It's assumed only one such color exists per region).
        vi. After the BFS for the region is complete: If `region_fill_color` is not `None`:
            *   Iterate through all pixels `(pr, pc)` recorded in `current_region_pixels`.
            *   If the pixel at `(pr, pc)` in the *original input grid* was White (0), change the color of the corresponding pixel in the `output_grid` to `region_fill_color`.
5.  **Return:** Return the modified output grid.
"""

def transform(input_grid):
    """
    Fills internal white regions based on the presence of a non-background, non-boundary color within that region.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # --- Define colors ---
    boundary_color = 8 # Azure
    background_color = 0 # White

    # --- 1. Identify External White Pixels ---
    visited_external = np.zeros_like(grid, dtype=bool)
    q_external = deque()

    # Add border white pixels to the external queue
    for r in range(rows):
        for c in range(cols):
            # Check if on border and is background color
            if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and grid[r, c] == background_color:
                if not visited_external[r, c]:
                    visited_external[r, c] = True
                    q_external.append((r, c))

    # BFS to find all externally connected white pixels
    while q_external:
        r, c = q_external.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == background_color and not visited_external[nr, nc]:
                visited_external[nr, nc] = True
                q_external.append((nr, nc))

    # --- 2. Identify and Process Internal Regions ---
    visited_internal = np.zeros_like(grid, dtype=bool)

    # Pre-mark boundaries and external white areas as visited for the internal search
    visited_internal[grid == boundary_color] = True
    visited_internal[visited_external] = True # Mark external white pixels as visited

    # Iterate through all pixels to find starting points for internal regions
    for r in range(rows):
        for c in range(cols):
            # If this pixel hasn't been visited (it's not boundary, not external white, and not part of a processed region)
            if not visited_internal[r, c]:
                # Start a new region discovery (BFS)
                current_region_pixels = []
                region_fill_color = None
                q_region = deque([(r, c)])
                
                # Mark the starting pixel as visited immediately
                visited_internal[r, c] = True 
                
                # Process the starting pixel itself
                current_region_pixels.append((r, c))
                pixel_color = grid[r, c]
                if pixel_color != background_color and pixel_color != boundary_color:
                     region_fill_color = pixel_color

                # Perform BFS to find all connected pixels in this internal region
                while q_region:
                    curr_r, curr_c = q_region.popleft()

                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is valid for this region
                        if 0 <= nr < rows and 0 <= nc < cols and not visited_internal[nr, nc]:
                            visited_internal[nr, nc] = True # Mark neighbor as visited
                            q_region.append((nr, nc))      # Add to queue for exploration
                            current_region_pixels.append((nr, nc)) # Add to current region list

                            # Check if this neighbor determines the fill color for the region
                            neighbor_color = grid[nr, nc]
                            if neighbor_color != background_color and neighbor_color != boundary_color:
                                region_fill_color = neighbor_color # Assume only one fill color per region

                # --- After BFS for the region is complete, fill if needed ---
                if region_fill_color is not None:
                    # Go through all pixels found in this region
                    for pr, pc in current_region_pixels:
                        # If the original pixel was background color, fill it in the output grid
                        if grid[pr, pc] == background_color:
                            output_grid[pr, pc] = region_fill_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```