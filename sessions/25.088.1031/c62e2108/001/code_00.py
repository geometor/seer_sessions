import numpy as np
from collections import deque

"""
Transforms the input grid based on pattern tiling rules indicated by blue markers.

1.  Identifies contiguous blocks of non-white (0) and non-blue (1) pixels ("patterns").
2.  Identifies horizontal (1x4) and vertical (4x1) lines of blue (1) pixels ("markers").
3.  Determines the association between markers and patterns: a marker is associated if it lies immediately adjacent to and perfectly aligned with one side of a pattern's bounding box.
4.  Initializes the output grid as a copy of the input grid.
5.  Removes all blue markers from the output grid by changing their color to white (0).
6.  For each pattern, based on its associated markers, tiles (repeats) the pattern's bounding box content (including background pixels within the box) in the indicated direction(s) (up, down, left, right).
7.  Tiling extends from the pattern's edge towards the grid boundary along the rows/columns defined by the pattern's bounding box.
8.  Returns the modified grid.
"""

def _find_connected_components(grid, ignore_colors=None):
    """Finds all connected components of the same color, ignoring specified colors."""
    if ignore_colors is None:
        ignore_colors = set()
    
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] not in ignore_colors:
                color = grid[r, c]
                component_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    component_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if component_pixels:
                    components.append({'color': color, 'pixels': component_pixels})
    return components

def _get_bounding_box(pixels):
    """Calculates the bounding box for a set of pixel coordinates."""
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    return min(rows), min(cols), max(rows), max(cols)

def _is_marker(component):
    """Checks if a blue component is a 1x4 or 4x1 marker."""
    if component['color'] != 1 or len(component['pixels']) != 4:
        return False, None # Not a potential marker

    pixels = sorted(list(component['pixels']))
    rows = sorted(list(set(r for r, c in pixels)))
    cols = sorted(list(set(c for r, c in pixels)))

    # Check for 1x4 horizontal marker
    if len(rows) == 1 and len(cols) == 4 and cols[-1] - cols[0] == 3:
         # Check contiguity
        expected_pixels = set((rows[0], c) for c in range(cols[0], cols[0] + 4))
        if component['pixels'] == expected_pixels:
             return True, 'horizontal'
            
    # Check for 4x1 vertical marker
    if len(rows) == 4 and len(cols) == 1 and rows[-1] - rows[0] == 3:
        # Check contiguity
        expected_pixels = set((r, cols[0]) for r in range(rows[0], rows[0] + 4))
        if component['pixels'] == expected_pixels:
            return True, 'vertical'

    return False, None

def transform(input_grid):
    """
    Applies the pattern tiling transformation.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Find all connected components
    all_components = _find_connected_components(input_np, ignore_colors={0}) # Ignore white initially

    # Identify patterns and markers
    patterns = []
    markers = []
    for comp in all_components:
        is_marker_flag, orientation = _is_marker(comp)
        if is_marker_flag:
            comp['orientation'] = orientation
            markers.append(comp)
        elif comp['color'] != 1: # Pattern if not white (ignored) and not blue (marker)
            bbox = _get_bounding_box(comp['pixels'])
            if bbox:
                comp['bbox'] = bbox
                patterns.append(comp)

    # --- State Change 1: Remove markers from the output grid ---
    for marker in markers:
        for r, c in marker['pixels']:
            output_np[r, c] = 0 # Set marker pixels to white

    # Store initial pattern tiles (after marker removal)
    initial_tiles = {}
    for i, pattern in enumerate(patterns):
        r_min, c_min, r_max, c_max = pattern['bbox']
        initial_tiles[i] = np.copy(output_np[r_min:r_max+1, c_min:c_max+1])


    # --- State Change 2: Tile patterns based on associated markers ---
    for i, pattern in enumerate(patterns):
        r_min, c_min, r_max, c_max = pattern['bbox']
        pattern_h = r_max - r_min + 1
        pattern_w = c_max - c_min + 1
        
        # Use the stored initial tile for copying
        tile_to_copy = initial_tiles[i] 

        # Check for associated markers and perform tiling
        associated_directions = set()

        for marker in markers:
            marker_pixels = marker['pixels']
            
            # Check Up Association
            if marker['orientation'] == 'horizontal':
                 marker_row = list(marker_pixels)[0][0] # All rows are the same
                 marker_cols = set(c for r,c in marker_pixels)
                 if marker_row == r_min - 1 and \
                    min(marker_cols) == c_min and max(marker_cols) == c_max:
                     associated_directions.add('up')

            # Check Down Association
            if marker['orientation'] == 'horizontal':
                 marker_row = list(marker_pixels)[0][0] 
                 marker_cols = set(c for r,c in marker_pixels)
                 if marker_row == r_max + 1 and \
                    min(marker_cols) == c_min and max(marker_cols) == c_max:
                     associated_directions.add('down')
            
            # Check Left Association
            if marker['orientation'] == 'vertical':
                 marker_col = list(marker_pixels)[0][1] # All cols are the same
                 marker_rows = set(r for r,c in marker_pixels)
                 if marker_col == c_min - 1 and \
                    min(marker_rows) == r_min and max(marker_rows) == r_max:
                     associated_directions.add('left')

            # Check Right Association
            if marker['orientation'] == 'vertical':
                 marker_col = list(marker_pixels)[0][1]
                 marker_rows = set(r for r,c in marker_pixels)
                 if marker_col == c_max + 1 and \
                    min(marker_rows) == r_min and max(marker_rows) == r_max:
                     associated_directions.add('right')


        # Perform tiling based on associated directions
        
        # Up Tiling
        if 'up' in associated_directions:
            curr_r = r_min - pattern_h
            while curr_r >= 0:
                # Check if target area is within bounds (redundant due to while condition?)
                if curr_r + pattern_h > 0:
                   # Ensure slicing doesn't go out of bounds upwards (curr_r could be negative if pattern_h large)
                   copy_start_row = max(0, curr_r)
                   tile_start_row = max(0, -curr_r)
                   copy_height = min(pattern_h, rows - copy_start_row) 
                   
                   # Adjust height if copy starts partway into the tile zone
                   copy_height = min(copy_height, pattern_h - tile_start_row) 

                   if copy_height > 0:
                       output_np[copy_start_row : copy_start_row + copy_height, c_min : c_min + pattern_w] = \
                           tile_to_copy[tile_start_row : tile_start_row + copy_height, :]
                curr_r -= pattern_h
                
        # Down Tiling
        if 'down' in associated_directions:
            curr_r = r_min + pattern_h # Start position for the *next* tile
            while curr_r < rows:
                # Check bounds for target area
                if curr_r + pattern_h <= rows: # Full tile fits
                    output_np[curr_r : curr_r + pattern_h, c_min : c_min + pattern_w] = tile_to_copy
                else: # Partial tile fits
                    copy_height = rows - curr_r
                    if copy_height > 0:
                       output_np[curr_r : curr_r + copy_height, c_min : c_min + pattern_w] = \
                           tile_to_copy[0 : copy_height, :]
                    break # No more space below
                curr_r += pattern_h

        # Left Tiling
        if 'left' in associated_directions:
            curr_c = c_min - pattern_w
            while curr_c >= 0:
                 if curr_c + pattern_w > 0:
                    copy_start_col = max(0, curr_c)
                    tile_start_col = max(0, -curr_c)
                    copy_width = min(pattern_w, cols - copy_start_col)
                    copy_width = min(copy_width, pattern_w - tile_start_col)
                    
                    if copy_width > 0:
                        output_np[r_min : r_min + pattern_h, copy_start_col : copy_start_col + copy_width] = \
                           tile_to_copy[:, tile_start_col : tile_start_col + copy_width]
                 curr_c -= pattern_w

        # Right Tiling
        if 'right' in associated_directions:
            curr_c = c_min + pattern_w # Start position for the *next* tile
            while curr_c < cols:
                if curr_c + pattern_w <= cols: # Full tile fits
                    output_np[r_min : r_min + pattern_h, curr_c : curr_c + pattern_w] = tile_to_copy
                else: # Partial tile fits
                    copy_width = cols - curr_c
                    if copy_width > 0:
                       output_np[r_min : r_min + pattern_h, curr_c : curr_c + copy_width] = \
                           tile_to_copy[:, 0 : copy_width]
                    break # No more space right
                curr_c += pattern_w


    # Convert final numpy array back to list of lists
    return output_np.tolist()