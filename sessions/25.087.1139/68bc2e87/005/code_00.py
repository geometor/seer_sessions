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
             set if no region is found from the start_coords.
    """
    rows, cols = grid.shape
    q = collections.deque()
    region_coords = set()

    # Initialize queue with valid starting points from start_coords
    for r, c in start_coords:
        # Check bounds, target color, and if already visited
        if 0 <= r < rows and 0 <= c < cols and \
           grid[r, c] == target_color and \
           not visited[r, c]:
            visited[r, c] = True  # Mark as visited
            q.append((r, c))
            region_coords.add((r, c))

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
                visited[nr, nc] = True # Mark as visited
                q.append((nr, nc))
                region_coords.add((nr, nc))

    return region_coords

def transform(input_grid_list):
    """
    Identifies a sequence of colors corresponding to nested contiguous regions
    within the input grid. The process starts by finding the azure (8) colored
    region connected to the grid's border. It then iteratively finds the next
    immediately adjacent, contiguous region of a single color inwards. The colors
    of these nested regions (excluding the initial azure background) are recorded.
    If the color red (2) is found anywhere in this sequence of region colors,
    the function outputs a 1x1 grid containing red ([[2]]). Otherwise, it outputs
    an empty grid ([]). If no azure background connected to the border exists,
    it also outputs an empty grid.
    """
    try:
        # Convert input list of lists to numpy array for efficient processing
        grid = np.array(input_grid_list, dtype=int)
        # Handle empty input grid
        if grid.size == 0:
            return []
        rows, cols = grid.shape
    except Exception:
        # Handle potential errors in input format, although ARC spec usually ensures lists of lists
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
            border_pixels.add((r, cols - 1))
        for c in range(cols):
            border_pixels.add((0, c))
            border_pixels.add((rows - 1, c))

    # Find starting points for the background region BFS (azure pixels on the border)
    background_start_coords = []
    for r, c in border_pixels:
         if grid[r, c] == background_color and not visited[r, c]:
             # Found an unvisited azure border pixel - add it as a starting point
             # No need to mark visited here; find_contiguous_region will do it
             background_start_coords.append((r,c))
             # Note: find_contiguous_region handles finding the full region even if
             # start points are disconnected initially, as long as they belong
             # to the same target_color region eventually connected.

    if not background_start_coords:
        # No azure background connected to the border was found.
        return []

    # Find the complete background region using BFS and mark it as visited
    current_region_pixels = find_contiguous_region(grid, background_start_coords, background_color, visited)

    # --- Step 2: Iteratively find nested regions inward ---
    region_color_sequence = [] # Stores the colors of the nested regions found

    while True:
        # Find all unique, unvisited neighbor coordinates adjacent to the current region
        neighbor_coords = set()
        for r, c in current_region_pixels:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check bounds and if the neighbor hasn't been visited yet
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]:
                    neighbor_coords.add((nr, nc))

        if not neighbor_coords:
            # No unvisited neighbors found, signifies the end of nesting
            break

        # Determine the colors present among these immediate neighbors
        neighbor_colors = set()
        neighbor_start_coords_by_color = collections.defaultdict(list)
        for nr, nc in neighbor_coords:
            color = grid[nr, nc]
            neighbor_colors.add(color)
            neighbor_start_coords_by_color[color].append((nr, nc))

        # Check if the neighbors form a single contiguous region of one color
        if len(neighbor_colors) != 1:
            # Ambiguous structure: multiple colors border the current region,
            # or the structure isn't perfectly nested layers. Stop processing.
            break

        # Get the color of the next layer
        next_layer_color = list(neighbor_colors)[0]

        # Record the color of this layer in the sequence
        region_color_sequence.append(next_layer_color)

        # Find the entire contiguous region of this next layer color using BFS
        # Start the search from all neighbor pixels of this color
        next_region_pixels = find_contiguous_region(grid,
                                                    neighbor_start_coords_by_color[next_layer_color],
                                                    next_layer_color,
                                                    visited)

        if not next_region_pixels:
            # Should not happen if neighbors were found, but acts as a safeguard.
            # Indicates an issue like visited state being wrong or BFS logic error.
            break

        # Update the current region for the next iteration
        current_region_pixels = next_region_pixels

    # --- Step 3: Check if the target color (Red 2) was found in the sequence ---
    if target_color in region_color_sequence:
        # Output a 1x1 grid containing the target color
        return [[target_color]]
    else:
        # Target color not found, or process stopped early; return empty grid
        return []