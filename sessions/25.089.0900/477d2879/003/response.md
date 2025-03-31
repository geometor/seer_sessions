```python
import numpy as np
from collections import deque
# Optional: from scipy.ndimage import label

"""
Transforms the input grid based on partitioning pixels into roles relative to blue(1) walls.
1.  Identify regions: 'reachable' (from border without crossing blue), 'enclosed' (not reachable).
2.  Categorize non-white(0), non-blue(1) 'active pixels' into:
    - 'Strictly_Enclosed': Active pixel in an enclosed region.
    - 'Adjacent': Active pixel in a reachable region, but 4-adjacent to a blue(1) pixel.
    - 'External': Active pixel in a reachable region, not adjacent to blue(1).
3.  Determine Wall Color: Blue(1) pixels change to Red(2) if Red(2) is the only non-Azure(8) color among all Strictly_Enclosed and Adjacent active pixels; otherwise, they change to Azure(8).
4.  Determine Fill Color: White(0) pixels in enclosed regions are filled based on the colors of Strictly_Enclosed active pixels (priority: Green(3) > Magenta(6) > Azure(8)). If no Strictly_Enclosed active pixels exist, use Adjacent active pixels with the same priority. Defaults to Azure(8).
5.  Fill Outside Area: White(0) pixels in reachable regions are filled using Voronoi tessellation based on External active pixels as seeds (Manhattan distance, tie-break by row then column).
6.  Active pixels generally retain their original color.
"""

def _find_reachable_pixels(grid):
    """
    Finds pixels reachable from the border without crossing blue (1) pixels.
    Uses Breadth-First Search (BFS) on non-blue cells starting from the border.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: A boolean mask where True indicates a reachable pixel.
    """
    rows, cols = grid.shape
    reachable_mask = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Add border cells that are not blue (1) to the queue and mark as reachable
    for r in range(rows):
        if grid[r, 0] != 1:
            if not reachable_mask[r, 0]:
                queue.append((r, 0))
                reachable_mask[r, 0] = True
        if grid[r, cols - 1] != 1:
             if not reachable_mask[r, cols - 1]:
                queue.append((r, cols - 1))
                reachable_mask[r, cols - 1] = True
    for c in range(1, cols - 1):
        if grid[0, c] != 1:
            if not reachable_mask[0, c]:
                queue.append((0, c))
                reachable_mask[0, c] = True
        if grid[rows - 1, c] != 1:
            if not reachable_mask[rows - 1, c]:
                queue.append((rows - 1, c))
                reachable_mask[rows - 1, c] = True

    # Perform BFS
    while queue:
        r, c = queue.popleft()

        # Check neighbors (4-directional)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if not already visited, and if not blue
            if 0 <= nr < rows and 0 <= nc < cols and \
               not reachable_mask[nr, nc] and grid[nr, nc] != 1:
                reachable_mask[nr, nc] = True
                queue.append((nr, nc))

    return reachable_mask

def _get_neighbors(pos, rows, cols):
    """Gets 4-directional neighbors within grid bounds."""
    r, c = pos
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def _categorize_active_pixels(grid, reachable_mask):
    """
    Categorizes active pixels (non-0, non-1) into Strictly_Enclosed, Adjacent, or External.

    Args:
        grid (np.ndarray): The input grid.
        reachable_mask (np.ndarray): Boolean mask of reachable pixels.

    Returns:
        tuple: Three lists of dictionaries: enclosed_active, adjacent_active, external_active.
               Each dictionary: {'pos': (r, c), 'color': color}
    """
    rows, cols = grid.shape
    enclosed_active = []
    adjacent_active = []
    external_active = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color != 1: # Is an active pixel
                pos = (r, c)
                is_reachable = reachable_mask[r, c]

                if not is_reachable:
                    enclosed_active.append({'pos': pos, 'color': color})
                else:
                    is_adjacent = False
                    for nr, nc in _get_neighbors(pos, rows, cols):
                        if grid[nr, nc] == 1:
                            is_adjacent = True
                            break
                    if is_adjacent:
                        adjacent_active.append({'pos': pos, 'color': color})
                    else:
                        external_active.append({'pos': pos, 'color': color})

    return enclosed_active, adjacent_active, external_active

def _manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    # Convert to numpy array and initialize output
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # --- Step 1 & 2: Identify Regions and Categorize Active Pixels ---
    reachable_mask = _find_reachable_pixels(grid)
    enclosed_active, adjacent_active, external_active = _categorize_active_pixels(grid, reachable_mask)

    # --- Step 3: Determine Transformation Colors ---

    # Wall Color Calculation
    wall_influencer_colors = set(p['color'] for p in enclosed_active) | set(p['color'] for p in adjacent_active)
    non_azure_wall_colors = wall_influencer_colors - {8} # Remove Azure(8) if present
    if non_azure_wall_colors == {2}: # Only Red(2) remains (or was the only one)
        wall_color = 2
    else:
        wall_color = 8 # Default to Azure

    # Fill Color Calculation
    fill_influencer_colors = set(p['color'] for p in enclosed_active)
    if not fill_influencer_colors: # If no strictly enclosed active pixels, use adjacent ones
         fill_influencer_colors = set(p['color'] for p in adjacent_active)

    fill_color = 8 # Default Azure
    if 3 in fill_influencer_colors:
        fill_color = 3
    elif 6 in fill_influencer_colors:
        fill_color = 6
    elif 8 in fill_influencer_colors: # Explicitly check if 8 is present for fill
         fill_color = 8
    # If none of 3, 6, 8 are present, it remains the default Azure(8)


    # --- Step 4: Apply Voronoi Fill for External Area ---
    seeds = external_active # Use only external pixels as seeds
    if seeds: # Only fill if there are seeds
        for r in range(rows):
            for c in range(cols):
                # Fill only reachable white pixels
                if reachable_mask[r, c] and grid[r, c] == 0:
                    min_dist = float('inf')
                    nearest_seeds = []
                    for seed in seeds:
                        dist = _manhattan_distance((r, c), seed['pos'])
                        if dist < min_dist:
                            min_dist = dist
                            nearest_seeds = [seed]
                        elif dist == min_dist:
                            nearest_seeds.append(seed)

                    # Tie-breaking: lowest row, then lowest column
                    best_seed = min(nearest_seeds, key=lambda s: (s['pos'][0], s['pos'][1]))
                    output_grid[r, c] = best_seed['color']

    # --- Step 5: Apply Wall and Enclosed Area Transformations ---
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1: # Original blue wall pixel
                output_grid[r, c] = wall_color
            elif grid[r, c] == 0 and not reachable_mask[r, c]: # Original enclosed white pixel
                output_grid[r, c] = fill_color

    # Active pixels retain original colors unless overwritten by wall color (handled by initialization and subsequent steps)

    return output_grid.tolist()
```