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
        print("Warning: skimage not found. Connected components analysis might be limited or inaccurate.")
        # Basic BFS/DFS based labeling could be implemented here as a fallback
        # For now, return an empty result to indicate failure.
        if return_num:
            return np.zeros_like(mask, dtype=int), 0
        else:
            return np.zeros_like(mask, dtype=int)

"""
Transformation Rule: Conditional Region Fill

1.  Identify the background color (most frequent).
2.  Find all contiguous non-background objects (using 4-way adjacency).
3.  Identify the largest object as the 'boundary' and others as 'other objects'.
4.  Determine if the boundary encloses any background pixels by performing a flood fill from the grid edges on background pixels. Unreached background pixels form the 'enclosed region'.
5.  If an enclosed region exists:
    a. Fill the enclosed region.
    b. The fill color is determined by the non-background, non-boundary pixels adjacent (8-way) to the enclosed region. Specifically, it's the most frequent color among these adjacent pixels. If no such pixels exist, or in case of a tie, a fallback might be needed (e.g., boundary color), though not explicitly required by examples.
6.  If no enclosed region exists:
    a. Fill the background pixels connected to the edge ('outside region').
    b. The fill color is the color of the smallest 'other object' by pixel count.
    c. If no 'other objects' exist, use the color of the boundary object as the fill color.
7.  Apply the determined fill color to the determined fill region, leaving all other pixels unchanged.
"""

def get_background_color(grid):
    """Determines the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default background for empty grid
    # Find the color with the maximum count
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_objects(grid, colors_to_ignore):
    """
    Finds connected components (objects) in the grid using 4-way connectivity,
    ignoring specified colors. Requires skimage.measure.label or a fallback.

    Args:
        grid (np.array): The input grid.
        colors_to_ignore (set): A set of color values to ignore.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'coords' (list of tuples), and 'size'.
              Sorted by size descending. Returns empty list if no objects found
              or if labeling fails.
    """
    objects = []
    unique_colors = np.unique(grid)
    rows, cols = grid.shape

    for color in unique_colors:
        if color in colors_to_ignore:
            continue

        mask = (grid == color)
        # Use connectivity=1 for 4-way adjacency
        labeled_mask, num_labels = label(mask, connectivity=1, background=0, return_num=True)

        # Handle case where skimage might not be available or fails
        if num_labels == 0 and np.any(mask):
             if not SKIMAGE_AVAILABLE:
                 print(f"Error: Cannot label objects of color {color} without skimage.")
                 # Potentially implement a fallback BFS/DFS labeler here if needed
             # else: # skimage is available but found 0 labels - should not happen if mask is not empty
                 # print(f"Warning: skimage.measure.label found 0 components for color {color} despite presence.")


        for i in range(1, num_labels + 1):
            coords = np.argwhere(labeled_mask == i)
            if coords.size == 0: continue # Skip if label somehow has no coords
            coords_list = [tuple(coord) for coord in coords]
            obj = {
                'color': color,
                'coords': coords_list,
                'size': len(coords_list)
            }
            objects.append(obj)

    # Sort objects primarily by size (descending)
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
            if (r,0) not in visited: queue.append((r, 0)); visited.add((r, 0))
        if grid[r, cols - 1] == background_color:
             if (r,cols-1) not in visited: queue.append((r, cols - 1)); visited.add((r, cols - 1))
    for c in range(1, cols - 1): # Avoid double-adding corners
        if grid[0, c] == background_color:
             if (0,c) not in visited: queue.append((0, c)); visited.add((0, c))
        if grid[rows - 1, c] == background_color:
             if (rows-1,c) not in visited: queue.append((rows - 1, c)); visited.add((rows - 1, c))

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
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Determine background color
    background_color = get_background_color(input_grid)

    # 2. Find all non-background objects
    all_objects = find_objects(input_grid, {background_color})

    # If no non-background objects, return the original grid
    if not all_objects:
        return input_grid_list

    # 3. Identify boundary object (largest) and other objects
    boundary_object = all_objects[0]
    boundary_coords_set = set(boundary_object['coords'])
    boundary_color = boundary_object['color'] # Assuming single color for boundary object
    other_objects = all_objects[1:]

    # 4. Find outside and enclosed background regions
    all_background_coords = set(tuple(coord) for coord in np.argwhere(input_grid == background_color))
    outside_background_coords = flood_fill_from_edge(input_grid, background_color)
    enclosed_background_coords = all_background_coords - outside_background_coords

    fill_target_coords = set()
    fill_color = -1 # Initialize with invalid color

    # 5. & 6. Determine fill type, target region, and fill color
    if enclosed_background_coords:
        # --- Inside Fill ---
        fill_target_coords = enclosed_background_coords

        # Find colors of non-background, non-boundary pixels adjacent (8-way) to the enclosed region
        adjacent_colors = []
        for r, c in enclosed_background_coords:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue # Skip self
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        pixel_coord = (nr, nc)
                        pixel_color = input_grid[nr, nc]
                        # Check if pixel is non-background and not part of the main boundary object
                        if pixel_color != background_color and pixel_coord not in boundary_coords_set:
                            adjacent_colors.append(pixel_color)

        if adjacent_colors:
            # Determine fill color: most frequent among adjacent non-boundary colors
            color_counts = Counter(adjacent_colors)
            fill_color = color_counts.most_common(1)[0][0]
        else:
            # Fallback: If no *other* objects are adjacent, maybe use boundary color?
            # Or perhaps a different rule applies? Example 3 has adjacent 'other' objects.
            # Let's default to boundary color as a plausible fallback.
            fill_color = boundary_color
            # print("Warning: Enclosed region found, but no non-boundary objects adjacent. Falling back to boundary color.")


    else:
        # --- Outside Fill ---
        fill_target_coords = outside_background_coords

        if other_objects:
            # Find smallest 'other object'
            smallest_other_object = min(other_objects, key=lambda o: o['size'])
            fill_color = smallest_other_object['color']
        else:
            # Fallback: No 'other objects', use boundary color
            fill_color = boundary_color
            # print("Warning: Outside fill required, but no 'other objects' found. Using boundary color.")

    # 7. Apply the fill
    if fill_color != -1 and fill_target_coords: # Ensure valid color and target found
        for r, c in fill_target_coords:
             # Check if the target coord is indeed background in the original grid
             # This check prevents accidentally overwriting parts of objects if logic is flawed
             # Although fill_target_coords should only contain background pixels by definition
             if input_grid[r,c] == background_color:
                  output_grid[r, c] = fill_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```