```python
"""
1. Initialize an output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Identify all distinct connected groups of azure (8) pixels in the input grid. These are the 'markers'. If no markers are found, return the initial white output grid.
3. Identify all distinct connected groups of pixels whose color is *not* white (0) and *not* azure (8). These are the 'source components'.
4. If no source components are found, return the initial white output grid.
5. Determine the single 'template pattern':
    a. Find the source component whose top-left corner coordinate has the minimum row index.
    b. If multiple source components share the minimum row index, select the one among them with the minimum column index. This is the 'primary source component'.
    c. Extract the shape of this primary source component within its own bounding box (treating pixels outside the component but within the box as background/white 0). This extracted shape is the 'template pattern'.
6. For each identified marker:
    a. Determine the coordinate (row, column) of its top-leftmost pixel.
    b. Copy ('stamp') the determined 'template pattern' onto the output grid, aligning the template's top-left corner with the marker's top-left coordinate.
    c. Ensure the template pattern is clipped if it extends beyond the output grid's boundaries during stamping. Pixels from the template overwrite the corresponding pixels in the output grid.
7. Return the final modified output grid.
"""

import numpy as np
from collections import deque

# Helper function to find connected components without scipy
def find_connected_components_no_scipy(grid, target_colors=None):
    """
    Finds all connected components for specified colors or all non-background colors
    using BFS, without relying on scipy.

    Args:
        grid (np.array): The input grid.
        target_colors (list or set, optional): A collection of integer colors
            to find objects for. If None, finds objects for all colors except 0.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (r, c) tuples),
              'bbox' (tuple: (min_r, min_c, max_r, max_c)), 'top_left' (r, c).
              Returns empty list if no objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    if target_colors is None:
        colors_present = np.unique(grid)
        target_colors = [c for c in colors_present if c != 0]
    if not target_colors:
        return objects

    target_colors_set = set(target_colors) # Faster lookup

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in target_colors_set and not visited[r, c]:
                # Start BFS for a new component
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds, color match, and visited status
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                if component_pixels:
                    objects.append({
                        'color': color,
                        'pixels': component_pixels,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'top_left': (min_r, min_c)
                    })

    # Sort objects primarily by top-left row, then column for consistent ordering
    objects.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    return objects

# Helper function to get the relative pattern of a component
def get_relative_pattern(component):
    """
    Extracts the relative pattern of a component within its bounding box.
    """
    color = component['color']
    pixels = component['pixels']
    min_r, min_c, max_r, max_c = component['bbox']
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    relative_pattern = np.zeros((height, width), dtype=int) # Use int type

    for r, c in pixels:
        relative_pattern[r - min_r, c - min_c] = color

    return relative_pattern

# Helper function to stamp a pattern onto the grid
def stamp_pattern(output_grid, pattern, top_left_coord):
    """
    Overlays the pattern onto the output grid at the specified coordinate,
    handling clipping.
    """
    r_start, c_start = top_left_coord
    p_h, p_w = pattern.shape
    g_h, g_w = output_grid.shape

    # Calculate the intersection bounds for stamping
    r_end = min(r_start + p_h, g_h)
    c_end = min(c_start + p_w, g_w)

    # Adjust start coordinates if they are negative (shouldn't happen with valid markers, but defensive)
    p_r_offset = 0
    p_c_offset = 0
    if r_start < 0:
        p_r_offset = -r_start
        r_start = 0
    if c_start < 0:
        p_c_offset = -c_start
        c_start = 0
        
    # Calculate slices for pattern and grid based on intersection and potential negative offset
    p_r_slice = slice(p_r_offset, p_r_offset + (r_end - r_start))
    p_c_slice = slice(p_c_offset, p_c_offset + (c_end - c_start))
    g_r_slice = slice(r_start, r_end)
    g_c_slice = slice(c_start, c_end)
    
    # Ensure slices are valid (have positive range) before attempting assignment
    # Also check if the calculated pattern slice dimensions match the grid slice dimensions
    if g_r_slice.start < g_r_slice.stop and g_c_slice.start < g_c_slice.stop and \
       (p_r_slice.stop - p_r_slice.start) == (g_r_slice.stop - g_r_slice.start) and \
       (p_c_slice.stop - p_c_slice.start) == (g_c_slice.stop - g_c_slice.start):
       
        # Create a mask for non-zero pixels in the pattern slice
        pattern_slice = pattern[p_r_slice, p_c_slice]
        mask = pattern_slice != 0 
        
        # Apply the pattern slice to the output grid using the mask
        output_grid[g_r_slice, g_c_slice][mask] = pattern_slice[mask]


def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # 1. Initialize output_grid
    output_grid = np.zeros_like(input_grid_np) # Filled with white (0)

    # 2. Find marker objects (color 8)
    marker_color = 8
    marker_objects = find_connected_components_no_scipy(input_grid_np, target_colors=[marker_color])

    # If no markers, return the initial white grid
    if not marker_objects:
        return output_grid.tolist()

    # 3. Find source objects (all colors except 0 and 8)
    all_colors = np.unique(input_grid_np)
    source_colors = [c for c in all_colors if c != 0 and c != marker_color]
    source_objects = find_connected_components_no_scipy(input_grid_np, target_colors=source_colors)

    # 4. If no source objects, return the initial white grid
    if not source_objects:
        return output_grid.tolist()

    # 5. Determine the template pattern
    # Objects are already sorted by top-left row, then column by find_connected_components
    primary_source_component = source_objects[0]
    template = get_relative_pattern(primary_source_component)

    # 6. Stamp the template for each marker
    for marker in marker_objects:
        marker_tl = marker['top_left']
        stamp_pattern(output_grid, template, marker_tl)

    # 7. Return the final grid as a list of lists
    return output_grid.tolist()
```