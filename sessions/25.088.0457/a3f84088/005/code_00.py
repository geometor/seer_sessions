import numpy as np
from collections import deque

"""
Transformation Rule:

1.  **Identify Regions:** Analyze the input grid to distinguish three types of pixels:
    *   The **frame**: Pixels with gray (5) color.
    *   The **exterior**: White (0) pixels that can reach the border of the grid through a path of only white pixels. These are identified using a Breadth-First Search (BFS) starting from all border white pixels.
    *   The **interior**: White (0) pixels that are *not* part of the exterior (i.e., they are enclosed by the frame).
2.  **Calculate Interior Distances:** Compute the minimum Manhattan distance (`d`) for each *interior* white pixel to the nearest gray (5) frame pixel. This is done using a BFS starting simultaneously from all frame pixels. The BFS only propagates through interior white pixels.
3.  **Determine Fill Colors:** For each *interior* white pixel, determine its output color based on its calculated distance `d` using the following cyclical pattern (modulo 4):
    *   If `d % 4 == 1`, set color to red (2).
    *   If `d % 4 == 2`, set color to gray (5).
    *   If `d % 4 == 3`, set color to white (0).
    *   If `d % 4 == 0`, set color to white (0).
4.  **Construct Output Grid:** Create the output grid. Initialize it as a copy of the input grid. Then, update the color of each *interior* white pixel according to the color determined in step 3. Leave the gray frame pixels and the exterior white pixels unchanged.
"""

def _identify_exterior_pixels(grid):
    """
    Identifies white (0) pixels connected to the grid border using BFS.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        set: A set of (row, col) tuples representing exterior white pixels.
    """
    rows, cols = grid.shape
    exterior_pixels = set()
    q = deque()

    # Add border white pixels (color 0) to the queue and the set
    for r in range(rows):
        if grid[r, 0] == 0 and (r, 0) not in exterior_pixels:
            q.append((r, 0))
            exterior_pixels.add((r, 0))
        # Check last column only if it exists and is different from the first
        if cols > 1 and grid[r, cols - 1] == 0 and (r, cols - 1) not in exterior_pixels:
            q.append((r, cols - 1))
            exterior_pixels.add((r, cols - 1))
            
    for c in range(cols): # Check full top/bottom rows
        if grid[0, c] == 0 and (0, c) not in exterior_pixels:
            q.append((0, c))
            exterior_pixels.add((0, c))
        # Check last row only if it exists and is different from the first
        if rows > 1 and grid[rows - 1, c] == 0 and (rows - 1, c) not in exterior_pixels:
            q.append((rows - 1, c))
            exterior_pixels.add((rows - 1, c))

    # Perform BFS to find all reachable white pixels from the border
    while q:
        r, c = q.popleft()
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if neighbor is white, and if not already identified as exterior
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0 and (nr, nc) not in exterior_pixels:
                exterior_pixels.add((nr, nc))
                q.append((nr, nc))
                
    return exterior_pixels

def _get_fill_color(distance):
    """
    Applies the coloring rule based on Manhattan distance to the frame.

    Args:
        distance (float): The Manhattan distance.

    Returns:
        int: The color value (0-9) for the pixel.
    """
    # Ensure distance is treated as an integer for modulo
    dist_int = int(distance)
    
    # Frame pixels (dist 0) or unreachable pixels (dist inf) retain original color
    if dist_int <= 0 or distance == np.inf:
        # This function should only be called for interior pixels with finite dist > 0.
        # Return white as a fallback if called inappropriately.
        return 0 

    remainder = dist_int % 4
    if remainder == 1:
        return 2 # red
    elif remainder == 2:
        return 5 # gray
    # elif remainder == 3:
    #     return 0 # white
    # elif remainder == 0: # distance is a multiple of 4
    #     return 0 # white
    else: # remainder is 0 or 3
        return 0 # white


def transform(input_grid):
    """
    Fills the interior white region enclosed by a gray frame based on the 
    Manhattan distance to the frame boundary, using a cyclical color pattern:
    dist % 4 = 1 -> red(2)
    dist % 4 = 2 -> gray(5)
    dist % 4 = 3 -> white(0)
    dist % 4 = 0 -> white(0)
    Exterior white pixels remain unchanged.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    rows, cols = input_grid_np.shape

    # 1. Identify Regions: Exterior White, Interior White, Frame
    exterior_white_pixels = _identify_exterior_pixels(input_grid_np)
    
    interior_white_pixels = set()
    frame_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid_np[r, c] == 0 and (r, c) not in exterior_white_pixels:
                interior_white_pixels.add((r, c))
            elif input_grid_np[r, c] == 5:
                frame_pixels.append((r,c))

    # If there are no interior pixels to color, return the original grid
    if not interior_white_pixels:
        return output_grid.tolist()
        
    # 2. Calculate Interior Distances using BFS from frame pixels
    # Initialize distances grid with infinity, except for frame pixels (distance 0)
    distances = np.full(input_grid_np.shape, np.inf)
    queue = deque()

    for r, c in frame_pixels:
        distances[r, c] = 0
        # Add frame pixels adjacent to interior white pixels to the queue to start BFS
        # This optimizes BFS slightly by not starting from frame pixels fully surrounded by other frame pixels
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
             nr, nc = r + dr, c + dc
             if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in interior_white_pixels:
                 # Check if this neighbor needs adding (first time seeing it from a frame pixel)
                 if distances[nr, nc] == np.inf:
                     distances[nr, nc] = 1 # Distance is 1 from the frame
                     queue.append(((nr, nc), 1)) # Add to queue with distance 1
                 # Optimization: No need to add the frame pixel itself to the main BFS queue if it has interior neighbors
                 # but we need to make sure all relevant interior pixels get queued if they touch the frame.
                 # The code above handles this: if an interior pixel (nr, nc) touches frame pixel (r, c),
                 # it will be added to the queue with distance 1.

    # If the queue is empty after initialization (e.g., frame completely surrounds nothing, or no interior pixels)
    # we might have missed frame pixels that were not adjacent to interior pixels. Re-initialize queue fully if needed.
    # However, the BFS below starts from the already queued neighbors (dist 1).
    # Let's refine the initialization to ensure all frame boundaries touching interior start the BFS correctly.
    # The previous logic was sufficient, but let's stick to a simpler BFS start: initialize all frame pixels.
    distances = np.full(input_grid_np.shape, np.inf)
    queue = deque()
    for r, c in frame_pixels:
        distances[r, c] = 0
        queue.append(((r, c), 0)) # Start BFS from all frame pixels

    processed_for_dist_calc = set(frame_pixels) # Keep track of pixels whose distances are finalized

    # Perform BFS, propagating distances through *interior* white pixels
    while queue:
        (r, c), dist = queue.popleft()

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds and if it's an *interior* white pixel
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in interior_white_pixels:
                 # If this interior pixel hasn't been reached yet (distance is inf)
                 if distances[nr, nc] == np.inf:
                     new_dist = dist + 1
                     distances[nr, nc] = new_dist
                     queue.append(((nr, nc), new_dist))
                     processed_for_dist_calc.add((nr,nc)) # Mark as processed for distance calc

    # 3. & 4. Determine Fill Colors and Construct Output Grid
    # Iterate through only the identified interior white pixels
    for r, c in interior_white_pixels:
        distance = distances[r,c]
        # Check if the pixel was reachable from the frame (distance is finite and > 0)
        if distance != np.inf and distance > 0:
             # Apply the coloring rule based on the calculated distance
             fill_color = _get_fill_color(distance)
             output_grid[r, c] = fill_color
        # else: 
             # If an interior pixel is unreachable (e.g., isolated white spot inside) 
             # or has dist 0 (shouldn't happen for interior pixels), leave it white (0).
             # It's already initialized as white from the copy, so no action needed.
             pass 

    return output_grid.tolist()