import numpy as np
from collections import deque, Counter

"""
Identifies contiguous shapes made of a primary non-white color that contain exactly one 'marker' pixel of a different non-white color.
For each such shape:
1. The border pixels of the primary color remain unchanged.
2. A diamond pattern, using the marker's color, expands outwards from the marker's location.
3. This pattern only colors pixels that were originally part of the shape's primary color area and are not on the border.
4. The expansion stops when the diamond layer no longer overlaps with the shape's non-border primary color area.
5. All original primary-colored pixels that are not on the border and not colored by the diamond pattern are set to white (0).
6. The original marker pixel location is also set to white (0).
Shapes without exactly one marker pixel remain unchanged.
"""

def find_shapes_and_markers(grid):
    """
    Finds connected non-white components, identifies primary color, 
    and checks for a single marker pixel.

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
                # Start BFS for a new connected component
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
                
                # Determine primary color (most frequent non-white color)
                # Filter out white just in case, though BFS shouldn't include it
                non_white_counts = {color: count for color, count in color_counts.items() if color != 0}
                if not non_white_counts:
                    continue
                
                primary_color = max(non_white_counts, key=non_white_counts.get)
                
                # Identify primary pixels and potential markers
                primary_pixels_set = set()
                marker_pixels = [] # List of (coord, color)
                for coord, color in component_pixels.items():
                    if color == primary_color:
                        primary_pixels_set.add(coord)
                    else:
                        marker_pixels.append((coord, color))

                # Check if exactly one marker pixel exists
                actual_marker_coord = None
                actual_marker_color = None
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
    Identifies the border pixels within a set of primary color pixels.

    Args:
        primary_pixels (set): Coordinates of pixels with the primary color.
        all_shape_pixels (set): Coordinates of all pixels in the shape component.
        grid_shape (tuple): (height, width) of the grid.

    Returns:
        set: Coordinates of the border pixels.
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
            # 2. Not part of the current shape's connected component.
            if not (0 <= nr < height and 0 <= nc < width) or \
               ((nr, nc) not in all_shape_pixels):
                 is_border = True
                 break
        if is_border:
            border_coords.add((r, c))
    return border_coords


def transform(input_grid):
    """
    Transforms the input grid by drawing hollow diamond patterns inside marked shapes.
    
    Identifies contiguous shapes made of a primary non-white color that contain exactly one 'marker' pixel of a different non-white color.
    For each such shape:
    1. The border pixels of the primary color remain unchanged.
    2. A diamond pattern, using the marker's color, expands outwards from the marker's location.
    3. This pattern only colors pixels that were originally part of the shape's primary color area and are not on the border.
    4. The expansion stops when the diamond layer no longer overlaps with the shape's non-border primary color area.
    5. All original primary-colored pixels that are not on the border and not colored by the diamond pattern are set to white (0).
    6. The original marker pixel location is also set to white (0).
    Shapes without exactly one marker pixel remain unchanged.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Find all shapes meeting the criteria
    shapes = find_shapes_and_markers(input_np)

    # Process each qualifying shape
    for shape in shapes:
        primary_pixels = shape['primary_pixels']
        primary_color = shape['primary_color'] # Not needed for output, but good context
        marker_coord = shape['marker_coord']
        marker_color = shape['marker_color']
        all_pixels_in_component = shape['all_pixels']
        
        # 1. Identify Border Pixels (these will remain primary_color)
        border_pixels = find_border_pixels(primary_pixels, all_pixels_in_component, (height, width))

        # 2. Identify Interior Primary Pixels (candidates for pattern or clearing)
        interior_primary_pixels = primary_pixels - border_pixels

        # 3. Expand diamond pattern from marker
        marker_r, marker_c = marker_coord
        pixels_colored_by_pattern = set()
        
        d = 1 # Start with Manhattan distance 1
        while True:
            colored_in_this_layer = False
            coords_at_distance_d = []

            # Generate coordinates at distance d
            for i in range(d + 1):
                j = d - i
                # Check all four quadrants relative to the marker
                coords_at_distance_d.append((marker_r + i, marker_c + j))
                if i != 0: coords_at_distance_d.append((marker_r - i, marker_c + j))
                if j != 0: coords_at_distance_d.append((marker_r + i, marker_c - j))
                if i != 0 and j != 0: coords_at_distance_d.append((marker_r - i, marker_c - j))
            
            # Filter and color valid coordinates within the interior
            potential_pixels_to_color_this_layer = set()
            for r, c in coords_at_distance_d:
                 # Check if the target pixel is an interior primary pixel
                 if (r,c) in interior_primary_pixels:
                     potential_pixels_to_color_this_layer.add((r, c))

            # Only proceed if there are pixels to color in this layer
            if not potential_pixels_to_color_this_layer:
                break # Stop expansion if diamond no longer overlaps interior

            # Color the identified pixels
            for r, c in potential_pixels_to_color_this_layer:
                output_np[r, c] = marker_color
                pixels_colored_by_pattern.add((r, c))
                colored_in_this_layer = True
            
            # It seems the expansion should stop *before* coloring if no valid pixels are found
            # The 'break' condition above handles this. If colored_in_this_layer remains false, loop terminates.

            d += 1 # Move to the next distance layer

        # 4. Clear remaining interior pixels (not border, not pattern) to white
        pixels_to_clear = interior_primary_pixels - pixels_colored_by_pattern
        for r, c in pixels_to_clear:
             # Check bounds just in case, though they should be within grid
             if 0 <= r < height and 0 <= c < width:
                 output_np[r, c] = 0
        
        # 5. Clear the original marker position to white
        mr, mc = marker_coord
        if 0 <= mr < height and 0 <= mc < width:
             output_np[mr, mc] = 0
             
        # Note: Border pixels were never modified from the initial output_np copy, 
        # so they retain their primary_color implicitly.

    return output_np.tolist()