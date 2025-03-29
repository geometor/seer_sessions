import numpy as np
from collections import deque

"""
The transformation rule involves a constrained flood fill operation originating from white pixels adjacent to gray pixels.

1.  **Identify Boundaries and Seeds:**
    *   Red pixels (2) and gray pixels (5) act as strict boundaries for the fill.
    *   White pixels (0) immediately adjacent (cardinally) to any gray pixel (5) are the starting points (seeds) for the fill.

2.  **Distinguish Inner vs. Outer White Pixels:**
    *   The grid contains white pixels (0) that are part of the general background ("outer") and white pixels that are enclosed or separated from the background by the red/gray boundaries ("inner").
    *   Only "inner" white pixels are potentially fillable.
    *   To identify "outer" pixels, perform a preliminary flood fill starting from all white pixels on the grid's border. This fill uses red and gray pixels as boundaries. Any white pixel reachable from the border is marked as "outer".

3.  **Perform Constrained Fill:**
    *   Initialize the output grid as a copy of the input grid.
    *   Start a Breadth-First Search (BFS) from the seed pixels identified in step 1.
    *   The BFS propagates cardinally (up, down, left, right).
    *   During the BFS, if a reachable pixel is:
        *   White (0) **and** was *not* marked as "outer" in step 2: Change its color to yellow (4) in the output grid and add it to the BFS queue.
        *   Red (2), Gray (5), or an "outer" white pixel: It acts as a boundary, stopping the fill along that path.
    *   Pixels already visited during the BFS are not processed again.

4.  **Final Output:**
    *   The output grid contains the original red and gray pixels, the "outer" white pixels remain white, and the "inner" white pixels reachable from the seeds are changed to yellow.
"""

def transform(input_grid):
    """
    Applies a bounded flood fill starting from neighbors of gray pixels,
    constrained to not fill the 'outer' background white space.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Define colors
    background_color = 0 # white (potentially fillable)
    boundary_color_1 = 2   # red (barrier)
    start_pixel_color = 5 # gray (origin point, also barrier)
    fill_color = 4       # yellow (fill result)

    # --- Step 1: Identify Outer Background ---
    is_outer_background = np.zeros_like(grid, dtype=bool)
    outer_queue = deque()
    outer_visited = set()

    # Add barriers to visited set for outer fill
    for r in range(height):
        for c in range(width):
            if grid[r, c] == boundary_color_1 or grid[r, c] == start_pixel_color:
                outer_visited.add((r, c))

    # Add border white pixels as starting points for outer fill
    for r in range(height):
        for c in [0, width - 1]: # Left and Right edges
            if (r, c) not in outer_visited and grid[r, c] == background_color:
                outer_visited.add((r, c))
                outer_queue.append((r, c))
                is_outer_background[r, c] = True
    for c in range(width):
        for r in [0, height - 1]: # Top and Bottom edges
             if (r, c) not in outer_visited and grid[r, c] == background_color:
                outer_visited.add((r, c))
                outer_queue.append((r, c))
                is_outer_background[r, c] = True

    # Perform BFS to mark all reachable outer background pixels
    while outer_queue:
        r, c = outer_queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in outer_visited:
                 if grid[nr, nc] == background_color: # Can only spread through white
                    outer_visited.add((nr, nc))
                    outer_queue.append((nr, nc))
                    is_outer_background[nr, nc] = True
                 else: # Hit a non-background color (barrier for this fill)
                     outer_visited.add((nr,nc)) # Mark non-white neighbors visited to prevent re-check

    # --- Step 2: Perform Main Fill ---
    main_queue = deque()
    main_visited = set()

    # Add barriers (red, gray) to visited set for main fill
    gray_coords = []
    for r in range(height):
        for c in range(width):
            pixel_color = grid[r, c]
            if pixel_color == start_pixel_color:
                main_visited.add((r, c))
                gray_coords.append((r,c))
            elif pixel_color == boundary_color_1:
                main_visited.add((r, c))
            # Also treat outer background as barrier for the main fill
            elif is_outer_background[r, c]:
                 main_visited.add((r, c))


    # Find initial white seed pixels adjacent to any gray pixel
    # These seeds must be "inner" white pixels (not outer background)
    for start_row, start_col in gray_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = start_row + dr, start_col + dc
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white, not already visited/queued for main fill,
                # AND not part of the outer background
                if grid[nr, nc] == background_color and \
                   (nr, nc) not in main_visited and \
                   not is_outer_background[nr, nc]:
                    # This is a valid seed pixel
                    output_grid[nr, nc] = fill_color
                    main_visited.add((nr, nc))
                    main_queue.append((nr, nc))

    # Perform flood fill using BFS from the identified seed pixels
    while main_queue:
        r, c = main_queue.popleft()

        # Explore cardinal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds and not visited for main fill
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in main_visited:
                 # Check if the neighbor is an original background color (white)
                 # AND it's NOT part of the outer background
                 if grid[nr, nc] == background_color and not is_outer_background[nr, nc]:
                     output_grid[nr, nc] = fill_color
                     main_visited.add((nr, nc))
                     main_queue.append((nr, nc))
                 else:
                     # Mark as visited even if it's a barrier (red, gray, outer background)
                     # to avoid checking it again
                     main_visited.add((nr, nc))

    # Convert the result back to a list of lists format
    return output_grid.tolist()