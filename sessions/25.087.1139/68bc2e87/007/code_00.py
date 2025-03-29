import numpy as np
import collections

def find_contiguous_region(grid, start_coords, target_color, visited):
    """
    Performs Breadth-First Search (BFS) to find all connected cells of a specific
    target_color starting from a set of initial coordinates (start_coords).

    It avoids cells marked as True in the `visited` array and updates `visited`
    in place for the newly found region cells. Orthogonal adjacency (up, down,
    left, right) is used for connectivity.

    Args:
        grid (np.array): The input grid.
        start_coords (iterable): An iterable of (row, col) tuples to start the BFS from.
                                 Only coords matching target_color and not visited
                                 will actually initiate the search.
        target_color (int): The color of the region to find.
        visited (np.array): A boolean array of the same shape as grid, marking
                             cells that have already been processed/visited.
                             This array is modified in place.

    Returns:
        set: A set of (row, col) tuples representing the coordinates of all
             cells belonging to the contiguous region found. Returns an empty
             set if no suitable starting point is found or if the region itself is empty.
    """
    rows, cols = grid.shape
    q = collections.deque()
    region_coords = set()

    # Initialize queue with valid starting points from start_coords
    processed_starts = set() # Keep track of starts added to avoid redundancy if start_coords has duplicates
    for r, c in start_coords:
        coord = (r, c)
        # Check bounds, target color, if already visited, and if already processed as a start point
        if 0 <= r < rows and 0 <= c < cols and \
           grid[r, c] == target_color and \
           not visited[r, c] and \
           coord not in processed_starts:
            visited[r, c] = True  # Mark as visited
            q.append(coord)
            region_coords.add(coord)
            processed_starts.add(coord) # Mark this specific start coord as processed

    # Perform BFS
    while q:
        r, c = q.popleft()

        # Explore neighbors (orthogonal)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, target color, and if already visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == target_color and \
               not visited[nr, nc]:
                visited[nr, nc] = True # Mark as visited *before* adding to queue
                q.append((nr, nc))
                region_coords.add((nr, nc))

    return region_coords

def transform(input_grid_list):
    """
    Identifies a sequence of colors corresponding to nested contiguous regions
    within the input grid, starting from an Azure (8) background connected to the
    border and moving inwards. The process stops if the next layer inwards is
    composed of multiple colors or if the innermost region is reached. If the
    color Red (2) is found in the sequence of identified layer colors, the
    function outputs a 1x1 grid containing Red ([[2]]). Otherwise, it outputs
    an empty grid ([]).
    """
    try:
        # Convert input list of lists to numpy array for efficient processing
        grid = np.array(input_grid_list, dtype=int)
        # Handle empty input grid immediately
        if grid.size == 0:
            return []
        rows, cols = grid.shape
    except Exception:
        # Handle potential errors in input format (though ARC spec usually ensures lists of lists)
        return []

    # Initialize a boolean grid to keep track of visited cells
    visited = np.zeros_like(grid, dtype=bool)
    background_color = 8 # Azure
    target_color = 2     # Red

    # --- Step 1: Find the initial Azure (8) background region connected to the border ---

    # Collect all unique border pixel coordinates
    border_pixels = set()
    if rows > 0 and cols > 0:
        for r in range(rows):
            border_pixels.add((r, 0))
            if cols > 1: # Avoid adding twice for 1-column grids
                 border_pixels.add((r, cols - 1))
        for c in range(cols):
            border_pixels.add((0, c))
            if rows > 1: # Avoid adding twice for 1-row grids
                border_pixels.add((rows - 1, c))

    # Find starting points for the background region BFS (azure pixels on the border)
    background_start_coords = []
    for r, c in border_pixels:
         # Check bounds (implicitly handled by border_pixels generation) and color
         if grid[r, c] == background_color:
             # Only need unvisited starting points; find_contiguous_region handles visited checks
             # Add all potential border starts of the correct color
             background_start_coords.append((r,c))

    # If no Azure pixels are found on the border, we cannot start.
    if not background_start_coords:
        return []

    # Find the complete background region using BFS and mark it as visited
    # Note: find_contiguous_region internally handles the visited array
    current_region_pixels = find_contiguous_region(grid, background_start_coords, background_color, visited)

    # If the background region itself couldn't be found (e.g., start points were already visited somehow?)
    if not current_region_pixels:
         return [] # Cannot proceed without a defined starting region

    # --- Step 2: Initialize sequence storage ---
    region_color_sequence = [] # Stores the colors of the nested regions found (excluding background)

    # --- Step 3 & 4: Iteratively find nested regions inward ---
    while True:
        # 4a. Find all unique, unvisited neighbor coordinates adjacent to the current region
        neighbor_coords = set()
        neighbor_start_coords_by_color = collections.defaultdict(list)

        for r, c in current_region_pixels:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check bounds and if the neighbor hasn't been visited yet
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]:
                    neighbor_coord = (nr, nc)
                    # Avoid processing the same neighbor multiple times in this iteration
                    if neighbor_coord not in neighbor_coords:
                       neighbor_coords.add(neighbor_coord)
                       color = grid[nr, nc]
                       neighbor_start_coords_by_color[color].append(neighbor_coord)

        # 4b. If no unvisited neighbors found, signifies the end of nesting
        if not neighbor_coords:
            break

        # 4c. Determine the colors present among these immediate neighbors
        neighbor_colors = list(neighbor_start_coords_by_color.keys())

        # 4d. Check if the neighbors form a single contiguous region of one color
        if len(neighbor_colors) != 1:
            # Ambiguous structure: multiple colors border the current region. Stop processing.
            break

        # 4e. Exactly one unique color found for the next layer
        next_layer_color = neighbor_colors[0]

        # 4e.i. Record the color of this layer in the sequence
        region_color_sequence.append(next_layer_color)

        # 4e.ii. Find the entire contiguous region of this next layer color using BFS
        # Start the search from all neighbor pixels of this color found earlier
        start_coords_for_next_layer = neighbor_start_coords_by_color[next_layer_color]
        next_region_pixels = find_contiguous_region(grid,
                                                    start_coords_for_next_layer,
                                                    next_layer_color,
                                                    visited)

        # Safety check: If BFS fails to find a region from valid starting points
        # (Should not happen if neighbors were found and BFS is correct, but good practice)
        if not next_region_pixels:
             # This indicates an unexpected state, potentially an error in logic or BFS.
             # Stop processing to avoid infinite loops or further errors.
             # Since we stop here, the target color might be missed if it was this layer.
             # The current sequence might be incomplete.
             break # Treat as unable to proceed cleanly

        # 4e.iii. Update the current region for the next iteration
        current_region_pixels = next_region_pixels

    # --- Step 5, 6, 7: Check if the target color (Red 2) was found in the sequence ---
    if target_color in region_color_sequence:
        # Output a 1x1 grid containing the target color
        return [[target_color]]
    else:
        # Target color not found, or process stopped early; return empty grid
        return []