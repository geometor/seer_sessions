import numpy as np
from collections import Counter, deque

# Attempt to import skimage, but provide a fallback if unavailable
try:
    from skimage.measure import label as skimage_label
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False
    # Define a simple placeholder or fallback labeler
    def skimage_label(mask, connectivity=1, background=0, return_num=False):
        """Basic BFS labeler as a fallback for skimage.measure.label."""
        rows, cols = mask.shape
        labeled_mask = np.zeros_like(mask, dtype=int)
        current_label = 0
        q = deque()
        # Define neighbors based on connectivity (1 -> 4-way, 2 -> 8-way)
        if connectivity == 1:
            neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        else: # Default to 8-way
             neighbors = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

        for r in range(rows):
            for c in range(cols):
                # If pixel is part of the mask and not yet labeled
                if mask[r, c] == 1 and labeled_mask[r, c] == 0:
                    current_label += 1
                    labeled_mask[r, c] = current_label
                    q.append((r, c))
                    # BFS for the current component
                    while q:
                        row, col = q.popleft()
                        for dr, dc in neighbors:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               mask[nr, nc] == 1 and labeled_mask[nr, nc] == 0:
                                labeled_mask[nr, nc] = current_label
                                q.append((nr, nc))
        if return_num:
            return labeled_mask, current_label
        else:
            return labeled_mask

"""
Transformation Rule (Hypothesis 6 - Revised):

1.  Identify the background color by finding the most frequent color in the input grid.
2.  Find all contiguous objects (shapes) of non-background colors using 4-way connectivity. Record each object's color, size, and coordinates.
3.  Determine the 'frame color' by finding the color of the largest object (by pixel count).
4.  Identify all objects whose color is *not* the background color and *not* the frame color. These are the 'other objects'. Collect coordinates of *all* non-background pixels to act as barriers for flood fill.
5.  **If** there are any 'other objects':
    a.  Find the 'signal object' among them that has the smallest size. If there's a tie in size, choose the one with the smallest color value.
    b.  The fill color is the color of this 'signal object'.
6.  **Else (if there are no 'other objects'):**
    a.  The fill color is the 'frame color'.
7.  Determine the 'base fill region': Perform a 4-way flood fill starting from all background pixels on the grid edges. The flood fill can only spread through background pixels and cannot cross *any* non-background pixel (using the collected barrier coordinates). Collect all reachable background coordinates.
8.  Determine the 'target fill region': If the 'base fill region' is not empty, find the first background pixel in it encountered when scanning the grid top-to-bottom, left-to-right. Perform a second 4-way flood fill starting from this pixel, restricted *only* to pixels within the 'base fill region'. The result is the 'target fill region'. If the base region is empty, the target region is also empty.
9.  Create the output grid by copying the input grid. Then, change the color of all pixels in the 'target fill region' to the determined fill color.
"""

def get_background_color(grid):
    """Determines the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default background for empty grid
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_objects(grid, colors_to_ignore):
    """
    Finds connected components (objects) in the grid using 4-way connectivity,
    ignoring specified colors.

    Args:
        grid (np.array): The input grid.
        colors_to_ignore (set): A set of color values to ignore.

    Returns:
        list: A list of dictionaries, each representing an object with
              'color', 'coords' (list of tuples), and 'size'. Sorted by size descending.
              Returns empty list if no objects found.
        set: A set containing the coordinates of all non-ignored pixels (barriers).
    """
    objects = []
    barrier_coords = set()
    unique_colors = np.unique(grid)
    rows, cols = grid.shape

    for color in unique_colors:
        if color in colors_to_ignore:
            continue

        mask = (grid == color)
        # Use connectivity=1 for 4-way adjacency for finding objects
        labeled_mask, num_labels = skimage_label(mask, connectivity=1, background=0, return_num=True)

        for i in range(1, num_labels + 1):
            coords = np.argwhere(labeled_mask == i)
            if coords.size == 0: continue
            coords_list = [tuple(coord) for coord in coords]
            obj = {
                'color': int(color), # Ensure color is standard int
                'coords': coords_list,
                'size': len(coords_list)
            }
            objects.append(obj)
            barrier_coords.update(coords_list) # Add object coords to barriers

    objects.sort(key=lambda o: o['size'], reverse=True)
    return objects, barrier_coords


def flood_fill_from_edge_with_barriers(grid, background_color, barrier_coords):
    """
    Performs flood fill from edge background pixels, stopping at barriers.
    Uses 4-way connectivity.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color to fill.
        barrier_coords (set): Set of (row, col) tuples that block the fill.

    Returns:
        set: Coordinates of background pixels reachable from the edge.
    """
    rows, cols = grid.shape
    visited = set()
    queue = deque()

    # Seed queue with edge background pixels not blocked by barriers
    for r in range(rows):
        if grid[r, 0] == background_color and (r, 0) not in barrier_coords:
            if (r, 0) not in visited: queue.append((r, 0)); visited.add((r, 0))
        if cols > 1 and grid[r, cols - 1] == background_color and (r, cols - 1) not in barrier_coords:
             if (r, cols - 1) not in visited: queue.append((r, cols - 1)); visited.add((r, cols - 1))
    for c in range(1, cols - 1):
        if grid[0, c] == background_color and (0, c) not in barrier_coords:
             if (0, c) not in visited: queue.append((0, c)); visited.add((0, c))
        if rows > 1 and grid[rows - 1, c] == background_color and (rows - 1, c) not in barrier_coords:
             if (rows - 1, c) not in visited: queue.append((rows - 1, c)); visited.add((rows - 1, c))
    # Handle 1x1 grid
    if rows == 1 and cols == 1 and grid[0,0] == background_color and (0,0) not in barrier_coords:
        if (0,0) not in visited: visited.add((0,0))

    # BFS
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4 neighbors
            nr, nc = r + dr, c + dc
            # Check bounds, background color, not visited, and not a barrier
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == background_color and \
               (nr, nc) not in visited and \
               (nr, nc) not in barrier_coords:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return visited

def find_connected_component(grid_shape, start_coord, allowed_coords):
    """
    Finds a connected component within a set of allowed coordinates starting from a point.
    Uses 4-way connectivity.

    Args:
        grid_shape (tuple): (rows, cols) of the grid.
        start_coord (tuple): (row, col) of the starting pixel.
        allowed_coords (set): Set of (row, col) tuples where the fill can spread.

    Returns:
        set: Coordinates of the connected component containing start_coord.
    """
    rows, cols = grid_shape
    if start_coord not in allowed_coords:
        return set()

    component = set()
    queue = deque([start_coord])
    component.add(start_coord)

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4 neighbors
            nr, nc = r + dr, c + dc
            coord = (nr, nc)
            # Check bounds, if it's an allowed coordinate, and not already in the component
            if 0 <= nr < rows and 0 <= nc < cols and \
               coord in allowed_coords and \
               coord not in component:
                component.add(coord)
                queue.append(coord)
    return component


def transform(input_grid_list):
    # Convert input to numpy array
    input_grid = np.array(input_grid_list, dtype=int)
    # Initialize output grid as a copy
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify background color
    background_color = get_background_color(input_grid)

    # 2. Find all non-background objects and barrier coordinates
    all_objects, barrier_coords = find_objects(input_grid, {background_color})

    # Handle edge case: only background exists
    if not all_objects:
        return input_grid_list

    # 3. Determine frame color (color of the largest object)
    frame_color = all_objects[0]['color']

    # 4. Identify 'other objects' (non-background, non-frame color)
    other_objects = [obj for obj in all_objects if obj['color'] != frame_color]

    # 5. & 6. Determine fill color
    fill_color = -1
    if other_objects:
        # Sort by size ascending, then color ascending for tie-breaking
        other_objects.sort(key=lambda o: (o['size'], o['color']))
        signal_object = other_objects[0]
        fill_color = signal_object['color']
    else:
        # No 'other objects', use frame color
        fill_color = frame_color

    # 7. Determine 'base fill region' (background reachable from edge, avoiding barriers)
    base_fill_region = flood_fill_from_edge_with_barriers(input_grid, background_color, barrier_coords)

    # 8. Determine 'target fill region' (component of base region containing first pixel)
    target_fill_region = set()
    start_pixel = None
    if base_fill_region:
        # Find the first pixel in scanline order
        for r in range(rows):
            for c in range(cols):
                if (r, c) in base_fill_region:
                    start_pixel = (r, c)
                    break
            if start_pixel:
                break
    
    if start_pixel:
        target_fill_region = find_connected_component((rows, cols), start_pixel, base_fill_region)

    # 9. Apply fill color to the target region in the output grid
    if fill_color != -1: # Ensure valid color was found
        for r, c in target_fill_region:
            # Check pixel is background before changing (safety check)
            if output_grid[r,c] == background_color:
                 output_grid[r, c] = fill_color

    # Convert back to list of lists for the required format
    return output_grid.tolist()