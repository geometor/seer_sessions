import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Initialization:** Create a copy of the input grid, which will become the output grid.
2.  **Identify Colors:** Determine the boundary color (Azure, 8), the background color (White, 0), and the fill color (the unique color present that is neither White nor Azure).
3.  **Identify External White Pixels:**
    a. Perform a Breadth-First Search (BFS) starting from all White (0) pixels located on the absolute border (edges) of the grid.
    b. Mark all reachable White (0) pixels during this BFS as 'external'. These are the white pixels connected to the outside of any Azure (8) boundaries.
4.  **Identify Fill Seeds:** Find all pixels in the input grid that initially have the fill color.
5.  **Perform Internal Flood Fill:**
    a. Perform a second BFS starting from the identified 'fill seed' pixels.
    b. During this BFS, explore adjacent pixels.
    c. If an adjacent pixel is White (0) in the input grid, has *not* been visited by *this* fill BFS, AND was *not* marked as 'external' in step 3:
        i. Change its color to the fill color in the output grid.
        ii. Mark it as visited for the fill BFS.
        iii. Add it to the fill BFS queue.
    d. This fill process stops at Azure (8) boundaries (as they are not White 0) and at the boundary between internal and external white pixels.
6.  **Return:** Return the modified output grid.
"""

def transform(input_grid):
    """
    Fills white regions connected to 'fill_color' pixels, constrained by 'boundary_color' 
    and not connected to the grid's outer border.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # --- 1. Identify boundary, background, and fill colors ---
    boundary_color = 8 # Azure
    background_color = 0 # White
    
    unique_colors = np.unique(grid)
    fill_color = -1
    for color in unique_colors:
        if color != background_color and color != boundary_color:
            fill_color = color
            break
            
    # If no specific fill color is found (only background/boundary or uniform grid), return original
    if fill_color == -1:
        return output_grid.tolist()

    # --- 2. Identify External White Pixels ---
    visited_external = np.zeros_like(grid, dtype=bool)
    q_external = deque()

    # Add border white pixels to the external queue
    for r in range(rows):
        for c in range(cols):
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

    # --- 3. Identify Fill Seeds and Initialize Fill BFS ---
    visited_fill = np.zeros_like(grid, dtype=bool)
    q_fill = deque()

    # Find all initial fill color pixels ("seeds") and add them to the fill queue
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == fill_color:
                # Seed points are implicitly "visited" for the fill process
                # but only add them to queue if not already processed (shouldn't happen here, but safe)
                if not visited_fill[r, c]:
                     visited_fill[r,c] = True # Mark seeds as visited for fill
                     q_fill.append((r,c)) 
                     # Ensure seed color is in output (already is from copy)
                     # output_grid[r, c] = fill_color 

    # --- 4. Perform Internal Flood Fill ---
    while q_fill:
        r, c = q_fill.popleft()

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is:
                # 1. Background color (White) in the *original* grid
                # 2. Not yet visited by *this* fill BFS
                # 3. Not part of the 'external' white region
                if grid[nr, nc] == background_color and \
                   not visited_fill[nr, nc] and \
                   not visited_external[nr, nc]:
                    
                    visited_fill[nr, nc] = True       # Mark as visited for fill
                    output_grid[nr, nc] = fill_color  # Change color in output
                    q_fill.append((nr, nc))           # Add to queue to explore its neighbors

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()