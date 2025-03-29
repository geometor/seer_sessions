```python
import numpy as np
from collections import deque, Counter

"""
Identifies contiguous shapes made of a primary non-white color (most frequent) 
that contain exactly one 'marker' pixel of a different non-white color.
For each such shape:
1. The border pixels of the primary color remain unchanged.
2. A hollow diamond pattern, using the marker's color, expands outwards from 
   the marker's location based on Manhattan distance.
3. This pattern only colors pixels that were originally part of the shape's 
   primary color area and are not on the border (interior primary pixels).
4. The expansion stops when the next diamond layer (at distance d) no longer 
   overlaps with any interior primary pixels.
5. All original interior primary pixels that are not colored by the final 
   hollow diamond pattern are set to white (0).
6. The original marker pixel location is also set to white (0).
Shapes without exactly one marker pixel, or components made entirely of one 
non-white color, remain unchanged.
Pixels outside of any processed shape remain unchanged.
"""

def find_shapes_and_markers(grid):
    """
    Finds connected non-white components, identifies primary color, 
    and checks for a single marker pixel. Uses 4-directional connectivity.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries for shapes meeting the criteria, containing:
              'primary_pixels': set of (row, col) tuples for the primary color pixels.
              'primary_color': the primary color of the shape.
              'marker_coord': (row, col) of the single marker, or None.
              'marker_color': color of the single marker, or None.
              'all_pixels': set of (row, col) tuples for all pixels in the component.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    shapes = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                # Start BFS for a new connected component (non-white pixels)
                q = deque([(r, c)])
                visited[r, c] = True
                component_pixels = {} # Store {coord: color}
                component_pixels[(r, c)] = grid[r, c]
                component_coords = set([(r, c)])

                while q:
                    row, col = q.popleft()
                    
                    # Check neighbors (4-directional connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] != 0:
                            
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_pixels[(nr, nc)] = grid[nr, nc]
                            component_coords.add((nr, nc))

                # Analyze the found component
                if not component_pixels:
                    continue

                color_counts = Counter(component_pixels.values())
                
                # Components must have at least two different colors to potentially have a marker
                if len(color_counts) < 2:
                    continue

                # Determine primary color (most frequent non-white color)
                primary_color = max(color_counts, key=color_counts.get)
                
                # Identify primary pixels and potential markers
                primary_pixels_set = set()
                marker_pixels = [] # List of (coord, color)
                for coord, color in component_pixels.items():
                    if color == primary_color:
                        primary_pixels_set.add(coord)
                    else: # Any other non-white color is a potential marker
                        marker_pixels.append((coord, color))

                # Check if exactly one marker pixel exists
                if len(marker_pixels) == 1:
                    actual_marker_coord, actual_marker_color = marker_pixels[0]
                    
                    # Store the shape details if it meets the criteria
                    shapes.append({
                        'primary_pixels': primary_pixels_set,
                        'primary_color': primary_color,
                        'marker_coord': actual_marker_coord,
                        'marker_color': actual_marker_color,
                        'all_pixels': component_coords # All coords in this connected component
                    })

    return shapes

def find_border_pixels(primary_pixels, all_shape_pixels, grid_shape):
    """
    Identifies the border pixels within a set of primary color pixels relative
    to the entire connected component. A primary pixel is border if it's 
    adjacent to a pixel outside the component or outside the grid.

    Args:
        primary_pixels (set): Coordinates of pixels with the primary color.
        all_shape_pixels (set): Coordinates of all pixels in the shape component.
        grid_shape (tuple): (height, width) of the grid.

    Returns:
        set: Coordinates of the border pixels among the primary_pixels.
    """
    height, width = grid_shape
    border_coords = set()
    for r, c in primary_pixels:
        is_border = False
        # Check 4 neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # A pixel is on the border if a neighbor is:
            # 1. Outside the grid boundaries.
            # 2. Not part of the current shape's connected component. (Includes white pixels)
            if not (0 <= nr < height and 0 <= nc < width) or \
               ((nr, nc) not in all_shape_pixels):
                 is_border = True
                 break
        if is_border:
            border_coords.add((r, c))
    return border_coords


def transform(input_grid):
    """
    Applies the hollow diamond transformation to qualifying shapes in the grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np) # Initialize output grid as a copy of input
    height, width = input_np.shape

    # 1. Identify Shapes and Markers
    shapes = find_shapes_and_markers(input_np)

    # 2. Process each qualifying shape
    for shape in shapes:
        primary_pixels = shape['primary_pixels']
        primary_color = shape['primary_color'] 
        marker_coord = shape['marker_coord']
        marker_color = shape['marker_color']
        all_pixels_in_component = shape['all_pixels']
        
        # 3a. Identify Border Pixels (these will remain primary_color)
        border_pixels = find_border_pixels(primary_pixels, all_pixels_in_component, (height, width))

        # 3b. Identify Interior Primary Pixels (candidates for pattern or clearing)
        interior_primary_pixels = primary_pixels - border_pixels

        # 3c. Generate Hollow Diamond Pattern
        marker_r, marker_c = marker_coord
        pixels_colored_by_pattern = set()
        
        d = 1 # Start with Manhattan distance 1
        while True:
            coords_at_distance_d = []
            # Generate coordinates exactly at distance d
            for i in range(d + 1):
                j = d - i
                # Add points in all four quadrants relative to the marker
                coords_at_distance_d.append((marker_r + i, marker_c + j))
                if i != 0: coords_at_distance_d.append((marker_r - i, marker_c + j))
                if j != 0: coords_at_distance_d.append((marker_r + i, marker_c - j))
                if i != 0 and j != 0: coords_at_distance_d.append((marker_r - i, marker_c - j))

            # Filter points: keep only those within grid bounds AND within the interior primary pixels
            target_pixels_this_layer = set()
            for r, c in coords_at_distance_d:
                 if 0 <= r < height and 0 <= c < width: # Check grid bounds explicitly
                     if (r, c) in interior_primary_pixels:
                         target_pixels_this_layer.add((r, c))

            # Stop expansion if this layer doesn't color any valid interior pixels
            if not target_pixels_this_layer:
                break 
            
            # Add the valid pixels of this layer to the final pattern set
            pixels_colored_by_pattern.update(target_pixels_this_layer)
            
            d += 1 # Move to the next distance layer

        # 4. Update the Output Grid for this shape
        
        # 4a. Color the pixels identified for the diamond pattern
        for r, c in pixels_colored_by_pattern:
            # Check bounds again just for safety, though filtering should handle it
            if 0 <= r < height and 0 <= c < width:
                 output_np[r, c] = marker_color
        
        # 4b. Clear remaining interior pixels (not border, not pattern) to white
        pixels_to_clear = interior_primary_pixels - pixels_colored_by_pattern
        for r, c in pixels_to_clear:
             if 0 <= r < height and 0 <= c < width:
                 output_np[r, c] = 0
        
        # 4c. Clear the original marker position to white
        mr, mc = marker_coord
        if 0 <= mr < height and 0 <= mc < width:
             # Ensure marker wasn't part of the border (unlikely but possible in weird shapes)
             # And ensure it wasn't part of the primary pixels (it shouldn't be by definition)
             # It should always be cleared.
             output_np[mr, mc] = 0
             
        # Note: Border pixels retain their primary color because they were in the initial
        # output_np copy and were not included in interior_primary_pixels, 
        # pixels_colored_by_pattern, or pixels_to_clear.

    # 5. Return the final grid
    return output_np.tolist()

```