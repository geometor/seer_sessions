```python
import numpy as np
from collections import Counter, deque

# Attempt to import skimage for connected components labeling
try:
    from skimage.measure import label
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False
    # Define a simple placeholder or raise an error if skimage is critical
    def label(mask, connectivity=1, background=0, return_num=False):
        """Placeholder for skimage.measure.label if not installed."""
        # This simple BFS labeler is a basic fallback.
        # It might be less efficient than skimage's implementation.
        rows, cols = mask.shape
        labeled_mask = np.zeros_like(mask, dtype=int)
        current_label = 0
        
        q = deque()
        
        # Define neighbors based on connectivity (1 -> 4-way, 2 -> 8-way)
        if connectivity == 1:
            neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        else: # Default to 8-way if not 1
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
Transformation Rule: Conditional Region Fill

1.  Identify the background color by finding the most frequent color in the input grid.
2.  Identify all contiguous objects (shapes) formed by non-background colors using 4-way connectivity. Record each object's color, size (pixel count), and coordinates.
3.  Determine the main boundary object: this is the object with the largest size. Note its color and coordinates.
4.  Identify all remaining non-background objects as 'other objects'.
5.  Perform a flood fill (using 4-way connectivity) starting from all background pixels located on the edges of the grid. The set of all reached background pixels constitutes the 'outside region'.
6.  Identify the 'enclosed region' by finding all background pixels that were *not* reached by the flood fill in step 5 (i.e., the set difference between all background pixels and the 'outside region').
7.  **If** the 'enclosed region' is non-empty:
    a.  The target for filling is the 'enclosed region'.
    b.  Determine the fill color: Examine all pixels adjacent (using 8-way connectivity) to any pixel in the 'enclosed region'. Collect the colors of these adjacent pixels, *excluding* the background color and any pixels belonging to the main boundary object identified in step 3. The fill color is the most frequent color among this collected set.
    c.  *Fallback:* If no such adjacent pixels are found (e.g., the enclosed region is only adjacent to the boundary and background), use the color of the main boundary object as the fill color.
8.  **Else (if the 'enclosed region' is empty):**
    a.  The target for filling is the 'outside region' (identified in step 5).
    b.  Determine the fill color: Find the object among the 'other objects' (from step 4) that has the smallest size. The fill color is the color of this smallest object.
    c.  *Fallback:* If there are no 'other objects', use the color of the main boundary object as the fill color.
9.  Create the output grid by copying the input grid. Then, for every coordinate in the determined fill target region (from step 7a or 8a), change the pixel color in the output grid to the determined fill color (from step 7b/c or 8b/c). Leave all other pixels unchanged.
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
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'coords' (list of tuples), and 'size'.
              Sorted by size descending. Returns empty list if no objects found.
    """
    objects = []
    unique_colors = np.unique(grid)
    rows, cols = grid.shape

    for color in unique_colors:
        if color in colors_to_ignore:
            continue

        mask = (grid == color)
        # Use connectivity=1 for 4-way adjacency for finding objects
        labeled_mask, num_labels = label(mask, connectivity=1, background=0, return_num=True)

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

    objects.sort(key=lambda o: o['size'], reverse=True)
    return objects

def flood_fill_from_edge(grid, background_color):
    """
    Performs a flood fill starting from background pixels at the grid edges
    using 4-way connectivity.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color of the background pixels to fill.

    Returns:
        set: A set of (row, col) tuples representing background pixels
             connected to the edge.
    """
    rows, cols = grid.shape
    visited = set()
    queue = deque()

    # Seed the queue with all background pixels on the border
    for r in range(rows):
        if grid[r, 0] == background_color:
            if (r, 0) not in visited: queue.append((r, 0)); visited.add((r, 0))
        if cols > 1 and grid[r, cols - 1] == background_color: # Check cols > 1 for 1D cases
             if (r, cols - 1) not in visited: queue.append((r, cols - 1)); visited.add((r, cols - 1))
    for c in range(1, cols - 1): # Avoid double-adding corners
        if grid[0, c] == background_color:
             if (0, c) not in visited: queue.append((0, c)); visited.add((0, c))
        if rows > 1 and grid[rows - 1, c] == background_color: # Check rows > 1
             if (rows - 1, c) not in visited: queue.append((rows - 1, c)); visited.add((rows - 1, c))
             
    # Handle 1x1 grid case separately if necessary
    if rows == 1 and cols == 1 and grid[0,0] == background_color:
        if (0,0) not in visited: visited.add((0,0))


    # Perform BFS using 4-way connectivity
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4 neighbors
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == background_color and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return visited

def transform(input_grid_list):
    """
    Applies the conditional region fill transformation based on whether the largest
    non-background object encloses a background region.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid_list, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Determine background color
    background_color = get_background_color(input_grid)

    # 2. Find all non-background objects (using 4-way connectivity)
    all_objects = find_objects(input_grid, {background_color})

    # Handle edge case: If no non-background objects, return original grid
    if not all_objects:
        return input_grid_list

    # 3. Identify boundary object (largest) and its properties
    boundary_object = all_objects[0]
    boundary_coords_set = set(boundary_object['coords'])
    # Assuming single color boundary for simplicity based on examples
    # If boundary could be multi-colored, this needs adjustment
    boundary_color = boundary_object['color']

    # 4. Identify other objects
    other_objects = all_objects[1:]

    # 5. Find background pixels connected to the edge (outside region) using 4-way flood fill
    all_background_coords = set(tuple(coord) for coord in np.argwhere(input_grid == background_color))
    outside_background_coords = flood_fill_from_edge(input_grid, background_color)

    # 6. Identify enclosed background pixels
    enclosed_background_coords = all_background_coords - outside_background_coords

    fill_target_coords = set()
    fill_color = -1 # Initialize with invalid color

    # 7. Check if an enclosed region exists and determine fill parameters
    if enclosed_background_coords:
        # --- Inside Fill ---
        fill_target_coords = enclosed_background_coords

        # Determine fill color based on 8-way adjacent non-background, non-boundary pixels
        adjacent_colors = []
        for r, c in enclosed_background_coords:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue # Skip self
                    nr, nc = r + dr, c + dc
                    # Check bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        pixel_coord = (nr, nc)
                        pixel_color = input_grid[nr, nc]
                        # Check if pixel is NOT background AND NOT part of the boundary object
                        if pixel_color != background_color and pixel_coord not in boundary_coords_set:
                            adjacent_colors.append(pixel_color)

        if adjacent_colors:
            # Fill color is the most frequent among valid adjacent colors
            color_counts = Counter(adjacent_colors)
            fill_color = color_counts.most_common(1)[0][0]
        else:
            # Fallback: Use boundary color if no valid adjacent pixels found
            fill_color = boundary_color

    # 8. Else (no enclosed region), determine parameters for outside fill
    else:
        # --- Outside Fill ---
        fill_target_coords = outside_background_coords

        if other_objects:
            # Fill color is from the smallest 'other object'
            # Need to handle potential ties in size - examples don't show this, pick first one
            smallest_other_object = min(other_objects, key=lambda o: o['size'])
            fill_color = smallest_other_object['color']
        else:
            # Fallback: Use boundary color if no 'other objects' exist
            fill_color = boundary_color

    # 9. Apply the fill to the output grid
    if fill_color != -1 and fill_target_coords: # Ensure valid color and target
        for r, c in fill_target_coords:
             # Check if the target coord is indeed background in the original grid
             # Redundant check as target coords are derived from background pixels, but safe
             if input_grid[r,c] == background_color:
                  output_grid[r, c] = fill_color

    # Convert final numpy grid back to list of lists
    return output_grid.tolist()
```