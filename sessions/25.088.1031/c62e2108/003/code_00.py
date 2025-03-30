import numpy as np
from collections import deque

"""
Tiles patterns across the grid based on instructions provided by aligned blue markers.

1. Identifies "patterns" (contiguous non-white, non-blue shapes) and their bounding boxes.
2. Identifies "markers" (4-pixel blue 1x4 or 4x1 lines) and their orientation/bounding boxes.
3. Creates a working copy of the grid.
4. Removes markers from the working grid (changes their pixels to white).
5. Extracts the "tile" (content within the pattern's bounding box) for each pattern from the marker-removed working grid.
6. Associates markers with patterns based on alignment:
    - Horizontal marker aligns if its column span matches the pattern's bbox column span. Direction is 'up' if marker is above pattern, 'down' if below.
    - Vertical marker aligns if its row span matches the pattern's bbox row span. Direction is 'left' if marker is left of pattern, 'right' if right.
7. For each pattern and its associated direction(s), tiles the extracted pattern tile repeatedly in that direction, starting from the pattern's edge, until the grid boundary is reached. Handles partial tiles at boundaries.
8. Returns the modified working grid.
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
    return min(rows), min(cols), max(rows), max(cols) # r_min, c_min, r_max, c_max

def _is_marker(component):
    """Checks if a blue component is a 1x4 or 4x1 marker."""
    if component['color'] != 1 or len(component['pixels']) != 4:
        return False, None, None # Not a potential marker

    bbox = _get_bounding_box(component['pixels'])
    if not bbox:
         return False, None, None

    r_min, c_min, r_max, c_max = bbox
    height = r_max - r_min + 1
    width = c_max - c_min + 1
    
    # Check for 1x4 horizontal marker
    if height == 1 and width == 4:
         # Extra check for contiguity just in case bbox calculation hides gaps, though unlikely with BFS
         is_contiguous = all((r_min, c) in component['pixels'] for c in range(c_min, c_max + 1))
         if is_contiguous:
             return True, 'horizontal', bbox

    # Check for 4x1 vertical marker
    if height == 4 and width == 1:
        # Extra check for contiguity
        is_contiguous = all((r, c_min) in component['pixels'] for r in range(r_min, r_max + 1))
        if is_contiguous:
             return True, 'vertical', bbox

    return False, None, None

def transform(input_grid):
    """
    Applies the pattern tiling transformation based on aligned markers.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # --- 1. Object Identification ---
    # Find all connected components, initially ignoring only white background
    all_components = _find_connected_components(input_np, ignore_colors={0}) 

    patterns = []
    markers = []
    # Identify patterns and markers from the components
    for comp in all_components:
        is_marker_flag, orientation, marker_bbox = _is_marker(comp)
        if is_marker_flag:
            comp['orientation'] = orientation
            comp['bbox'] = marker_bbox
            markers.append(comp)
        elif comp['color'] != 1: # Pattern if not white (ignored) and not blue (marker candidate)
            bbox = _get_bounding_box(comp['pixels'])
            if bbox:
                comp['bbox'] = bbox
                patterns.append(comp)

    # --- 2. Marker Removal ---
    # Modify the output grid by changing marker pixels to white
    for marker in markers:
        for r, c in marker['pixels']:
            if 0 <= r < rows and 0 <= c < cols: # Bounds check just in case
                output_np[r, c] = 0 

    # --- 3. Tile Extraction ---
    # Extract tiles *after* markers are removed
    pattern_tiles = {}
    for i, pattern in enumerate(patterns):
        r_min, c_min, r_max, c_max = pattern['bbox']
        # Ensure slicing is within bounds if bbox touches edge
        r_start, r_end = max(0, r_min), min(rows, r_max + 1)
        c_start, c_end = max(0, c_min), min(cols, c_max + 1)
        if r_start < r_end and c_start < c_end: # Check if valid dimensions remain
            pattern_tiles[i] = np.copy(output_np[r_start:r_end, c_start:c_end])
        else:
             pattern_tiles[i] = None # Handle edge case where pattern might be off-grid? (unlikely)

    # --- 4. Association and Tiling ---
    for i, pattern in enumerate(patterns):
        if pattern_tiles[i] is None: # Skip if tile couldn't be extracted
            continue
            
        p_r_min, p_c_min, p_r_max, p_c_max = pattern['bbox']
        tile_to_copy = pattern_tiles[i]
        pattern_h, pattern_w = tile_to_copy.shape
        
        # Find associated directions based on alignment
        associated_directions = set()
        for marker in markers:
            m_r_min, m_c_min, m_r_max, m_c_max = marker['bbox']
            
            # Check Horizontal Marker Alignment (Up/Down)
            if marker['orientation'] == 'horizontal':
                 # Check if column spans align
                 if m_c_min == p_c_min and m_c_max == p_c_max:
                     # Check relative row position
                     if m_r_min < p_r_min: # Marker is above pattern
                         associated_directions.add('up')
                     elif m_r_min > p_r_max: # Marker is below pattern
                         associated_directions.add('down')

            # Check Vertical Marker Alignment (Left/Right)
            elif marker['orientation'] == 'vertical':
                 # Check if row spans align
                 if m_r_min == p_r_min and m_r_max == p_r_max:
                     # Check relative column position
                     if m_c_min < p_c_min: # Marker is left of pattern
                         associated_directions.add('left')
                     elif m_c_min > p_c_max: # Marker is right of pattern
                         associated_directions.add('right')

        # Perform tiling for each associated direction
        
        # Up Tiling
        if 'up' in associated_directions:
            curr_r = p_r_min - pattern_h # Start row for the top-left corner of the first tile *above*
            while curr_r + pattern_h > 0: # While *any part* of the tile is potentially on grid upwards
                target_r_start = max(0, curr_r)
                target_r_end = min(rows, curr_r + pattern_h)
                tile_r_start = max(0, -curr_r) # Which part of the source tile to copy
                tile_r_end = tile_r_start + (target_r_end - target_r_start)

                if target_r_start < target_r_end: # If there's vertical space to copy into
                     output_np[target_r_start : target_r_end, p_c_min : p_c_min + pattern_w] = \
                         tile_to_copy[tile_r_start : tile_r_end, :]
                
                if curr_r < 0: # Optimization: if we started partially off grid, we are done upwards
                    break
                    
                curr_r -= pattern_h # Move to the next position above

        # Down Tiling
        if 'down' in associated_directions:
            curr_r = p_r_max + 1 # Start row for the top-left corner of the first tile *below*
            while curr_r < rows: # While the starting row is within the grid
                target_r_start = curr_r
                target_r_end = min(rows, curr_r + pattern_h)
                tile_r_end = target_r_end - target_r_start # How much vertical height to copy from tile

                if tile_r_end > 0:
                    output_np[target_r_start : target_r_end, p_c_min : p_c_min + pattern_w] = \
                        tile_to_copy[0 : tile_r_end, :]
                
                curr_r += pattern_h # Move to the next position below
                if target_r_end == rows: # Optimization: if we hit the bottom edge, we are done
                    break

        # Left Tiling
        if 'left' in associated_directions:
            curr_c = p_c_min - pattern_w # Start col for the top-left corner of the first tile *left*
            while curr_c + pattern_w > 0: # While *any part* of the tile is potentially on grid leftwards
                target_c_start = max(0, curr_c)
                target_c_end = min(cols, curr_c + pattern_w)
                tile_c_start = max(0, -curr_c) # Which part of the source tile to copy
                tile_c_end = tile_c_start + (target_c_end - target_c_start)

                if target_c_start < target_c_end: # If there's horizontal space to copy into
                     output_np[p_r_min : p_r_min + pattern_h, target_c_start : target_c_end] = \
                         tile_to_copy[:, tile_c_start : tile_c_end]
                
                if curr_c < 0: # Optimization
                    break
                    
                curr_c -= pattern_w # Move to the next position left

        # Right Tiling
        if 'right' in associated_directions:
            curr_c = p_c_max + 1 # Start col for the top-left corner of the first tile *right*
            while curr_c < cols: # While the starting col is within the grid
                target_c_start = curr_c
                target_c_end = min(cols, curr_c + pattern_w)
                tile_c_end = target_c_end - target_c_start # How much horizontal width to copy

                if tile_c_end > 0:
                    output_np[p_r_min : p_r_min + pattern_h, target_c_start : target_c_end] = \
                        tile_to_copy[:, 0 : tile_c_end]
                
                curr_c += pattern_w # Move to the next position right
                if target_c_end == cols: # Optimization
                    break


    # --- 5. Output ---
    # Convert final numpy array back to list of lists
    return output_np.tolist()