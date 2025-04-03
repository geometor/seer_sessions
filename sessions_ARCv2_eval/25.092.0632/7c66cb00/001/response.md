```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1.  Identify horizontal bands in the input grid. The top-most band containing multiple colors is the 'source' band. Bands below the source, characterized by a distinct frame color (1-pixel border) and a background color (inner area), are 'target' bands.
2.  Identify contiguous objects (non-background color) in the source band. Filter out objects completely enclosed within another object.
3.  Initialize the output grid as a copy of the input grid.
4.  Clear the source band area in the output grid, filling it with the source band's background color.
5.  For each target band:
    a. If the target band's background color is yellow (4): Find all yellow pixels in the original source band and draw them (using the target band's frame color) onto the corresponding locations in the output grid.
    b. If the target band's background color is NOT yellow:
        i. Find the primary source object(s) whose color matches the target band's background color.
        ii. If multiple matching objects exist, select the largest one (by pixel count).
        iii. If a matching object is found, draw its shape (using the target band's frame color) onto the corresponding locations in the output grid.
"""

# Helper function to find connected components (objects) using BFS
def find_objects(grid_region, background_color):
    """Finds connected objects of non-background color in a grid region."""
    objects = []
    visited = set()
    rows, cols = grid_region.shape

    for r in range(rows):
        for c in range(cols):
            if grid_region[r, c] != background_color and (r, c) not in visited:
                obj_color = grid_region[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-way connectivity ok? Let's try 8-way
                    # for dr in range(-1, 2):
                    #    for dc in range(-1, 2):
                    #        if dr == 0 and dc == 0:
                    #            continue
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and \
                           grid_region[nr, nc] == obj_color:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                
                # Check 8-way connectivity for merging later if needed, but build with 4-way first.
                # Re-checking example 1: source object looks 4-way connected.
                # Example 2: source objects look 4-way connected.
                # Example 3: source objects look 4-way connected.
                # Sticking with 4-way connectivity for object definition.

                objects.append({
                    'color': obj_color,
                    'coords': obj_coords,
                    'size': len(obj_coords),
                    'min_r': min(r for r, c in obj_coords),
                    'max_r': max(r for r, c in obj_coords),
                    'min_c': min(c for r, c in obj_coords),
                    'max_c': max(c for r, c in obj_coords),
                })
    return objects

# Helper function to check if an object is enclosed within another
def is_enclosed(obj_a, obj_b, grid_region):
    """Check if obj_a is fully enclosed by obj_b using adjacency."""
    # Quick check: B must be larger and contain A's bounding box (approx)
    if obj_a['size'] >= obj_b['size']:
        return False
    if not (obj_b['min_r'] <= obj_a['min_r'] and
            obj_b['max_r'] >= obj_a['max_r'] and
            obj_b['min_c'] <= obj_a['min_c'] and
            obj_b['max_c'] >= obj_a['max_c']):
        return False

    rows, cols = grid_region.shape
    # Check every neighbor of every pixel in obj_a
    for r, c in obj_a['coords']:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                neighbor_coord = (nr, nc)

                # If neighbor is outside grid, A is not enclosed
                if not (0 <= nr < rows and 0 <= nc < cols):
                    return False

                # If neighbor is not part of A and not part of B, A is not enclosed by B
                if neighbor_coord not in obj_a['coords'] and neighbor_coord not in obj_b['coords']:
                    return False
    return True


# Helper function to identify bands
def identify_bands(grid):
    """Identifies source and target bands based on structure."""
    rows, cols = grid.shape
    bands = []
    current_band_start = 0
    in_band = False

    # Find potential band boundaries (often rows of uniform color, but not always reliable)
    # Let's simplify: Identify bands by changes in row patterns or uniform rows.
    # Find the first row with multiple colors - this starts the source band region search
    source_band_info = None
    target_bands_info = []
    
    first_multi_color_row = -1
    for r in range(rows):
        if len(np.unique(grid[r, :])) > 1:
            first_multi_color_row = r
            break
    
    if first_multi_color_row == -1: # No multi-color rows found
        return None, []

    # --- Source Band Identification ---
    # Assume source band starts at first_multi_color_row and extends downwards
    # until a significant change (e.g., a fully uniform row, or a framed structure starts)
    # Need a heuristic for source background color. Maybe the most common color?
    source_start_row = first_multi_color_row
    source_end_row = source_start_row
    potential_source_bg = grid[source_start_row, 0] # Guess based on corner? Risky.
    
    # Iterate downwards to find the end of the source band.
    # Look for a uniform row or the start of a framed band.
    
    # Let's try finding the background color by checking corners or edges first.
    # In example 1, source bg is 1. In example 2, source bg is 8. In example 3, source bg is 4.
    # It seems to be the dominant color in the source band region that is NOT part of the internal objects.
    # Let's find the extent of the multi-color region first.
    
    current_row = first_multi_color_row
    while current_row < rows and len(np.unique(grid[current_row, :])) > 1:
         current_row += 1
    source_end_row = current_row -1 # Last row that had multiple colors (part of source)
    
    # Determine source background color within source_start_row to source_end_row
    source_region_pixels = grid[source_start_row:source_end_row+1, :].flatten()
    colors, counts = np.unique(source_region_pixels, return_counts=True)
    source_bg_guess = colors[np.argmax(counts)] # Most frequent color in the region
    
    # Refine background color: Find objects first, then bg is most common color NOT in objects?
    temp_source_region = grid[source_start_row:source_end_row+1, :]
    temp_objects = find_objects(temp_source_region, -1) # Find all objects initially assuming no bg
    object_colors = set(obj['color'] for obj in temp_objects)
    
    # Find most frequent color in the region that isn't an object color
    bg_candidate_counts = {}
    for r in range(source_start_row, source_end_row + 1):
        for c in range(cols):
             pixel_color = grid[r,c]
             if pixel_color not in object_colors:
                 bg_candidate_counts[pixel_color] = bg_candidate_counts.get(pixel_color, 0) + 1

    if not bg_candidate_counts: # Should not happen if region has >1 color
         source_bg = source_bg_guess # Fallback
    else:
         source_bg = max(bg_candidate_counts, key=bg_candidate_counts.get)

    source_band_info = {
        'start_row': source_start_row,
        'end_row': source_end_row,
        'background_color': source_bg
    }
    
    # --- Target Band Identification ---
    current_row = source_end_row + 1
    while current_row < rows:
        # Skip uniform rows (separators)
        while current_row < rows and len(np.unique(grid[current_row, :])) == 1:
            current_row += 1
        
        if current_row >= rows:
            break
            
        target_start_row = current_row
        
        # Check for frame structure: is grid[r, 0] != grid[r, 1]?
        frame_color_candidate = grid[target_start_row, 0]
        background_color_candidate = grid[target_start_row, 1] # Inner color
        
        # Verify frame/background consistency for a few rows
        is_framed_band = True
        band_end_row = target_start_row
        while band_end_row < rows:
            # Check if row pattern is consistent (frame/bg or all frame if width=1/2)
            row_colors = np.unique(grid[band_end_row, :])
            
            # End condition 1: Hit a uniform row that is not the frame color (separator)
            if len(row_colors) == 1 and row_colors[0] != frame_color_candidate:
                 band_end_row -= 1 # Previous row was the end
                 break
            
            # End condition 2: Hit a row with a different pattern (start of new band type)
            if grid[band_end_row, 0] != frame_color_candidate or \
               (cols > 1 and grid[band_end_row, 1] != background_color_candidate and grid[band_end_row, 1] != frame_color_candidate) or \
               (cols > 1 and grid[band_end_row, -1] != frame_color_candidate) or \
               (cols > 2 and grid[band_end_row, -2] != background_color_candidate and grid[band_end_row, -2] != frame_color_candidate):
                 # Check if it's just the end of the grid
                 if band_end_row + 1 == rows:
                    # If the last row matches the pattern, include it
                    pass
                 else:
                    # If pattern breaks mid-grid, end the band here
                    band_end_row -= 1 # Previous row was the end
                    break

            # Check corners and inner sample
            if grid[band_end_row, 0] != frame_color_candidate: is_framed_band=False; break
            if cols > 1 and grid[band_end_row, -1] != frame_color_candidate: is_framed_band=False; break
            if cols > 2 and grid[band_end_row, 1] != background_color_candidate:
                # Allow for case where inner area is filled with frame color temporarily by drawing
                # Check if the center-ish color matches background
                center_col = cols // 2
                if grid[band_end_row, center_col] != background_color_candidate and grid[band_end_row, center_col] != frame_color_candidate:
                    # If center doesn't match bg OR frame, it's likely a different band type
                     band_end_row -= 1
                     break

            band_end_row += 1
            
        # Ensure band_end_row didn't go past grid boundary
        band_end_row = min(band_end_row, rows - 1)

        # Validate that we actually found a framed band
        if is_framed_band and band_end_row >= target_start_row:
             # Check inner area to confirm background color if possible
             inner_region = grid[target_start_row:band_end_row+1, 1:cols-1]
             if inner_region.size > 0:
                 inner_colors, inner_counts = np.unique(inner_region, return_counts=True)
                 # Background should be the most common color unless it's empty
                 # Or maybe the color present at [start_row, 1]
                 confirmed_background = grid[target_start_row, 1] # Use the initial candidate
                 
                 target_bands_info.append({
                     'start_row': target_start_row,
                     'end_row': band_end_row,
                     'frame_color': frame_color_candidate,
                     'background_color': confirmed_background
                 })
             elif cols <= 2: # Handle thin bands
                 target_bands_info.append({
                     'start_row': target_start_row,
                     'end_row': band_end_row,
                     'frame_color': frame_color_candidate,
                     'background_color': background_color_candidate # May be same as frame
                 })


        current_row = band_end_row + 1

    return source_band_info, target_bands_info


def transform(input_grid_in):
    """
    Transforms the input grid by identifying source/target bands, finding objects
    in the source, and drawing selected object shapes/pixels into target bands
    based on color matching rules.
    """
    input_grid = np.array(input_grid_in, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Bands
    source_band, target_bands = identify_bands(input_grid)

    if source_band is None:
        # No source band found, return copy of input
        return output_grid.tolist()

    # 2. Analyze Source Band
    source_region = input_grid[source_band['start_row']:source_band['end_row'] + 1, :]
    all_source_objects = find_objects(source_region, source_band['background_color'])

    # 3. Filter out enclosed objects
    primary_source_objects = []
    potential_enclosed = list(range(len(all_source_objects)))
    
    for i in range(len(all_source_objects)):
        is_i_enclosed = False
        for j in range(len(all_source_objects)):
            if i == j:
                continue
            # Check if object i is enclosed by object j
            # Need relative coordinates within the source_region for is_enclosed
            if is_enclosed(all_source_objects[i], all_source_objects[j], source_region):
                 is_i_enclosed = True
                 break
        if not is_i_enclosed:
            primary_source_objects.append(all_source_objects[i])

    # 4. Clear Source in Output
    output_grid[source_band['start_row']:source_band['end_row'] + 1, :] = source_band['background_color']

    # 5. Process Target Bands
    for target in target_bands:
        target_bg = target['background_color']
        target_frame = target['frame_color']

        # 5a. Special Yellow Rule
        if target_bg == 4: # Yellow
            yellow_coords_in_source = []
            for r_rel, c_rel in np.argwhere(source_region == 4):
                r_abs = r_rel + source_band['start_row']
                c_abs = c_rel # Assuming source starts at col 0
                yellow_coords_in_source.append((r_abs, c_abs))
            
            # Draw these coordinates onto the output grid
            for r, c in yellow_coords_in_source:
                 # Check bounds just in case (should match source band location)
                 if target['start_row'] <= r <= target['end_row'] and 0 <= c < cols:
                     output_grid[r, c] = target_frame

        # 5b. Standard Processing
        else:
            matching_objects = [obj for obj in primary_source_objects if obj['color'] == target_bg]

            if not matching_objects:
                continue # No matching object found

            # Select the largest object if multiple match
            selected_object = None
            if len(matching_objects) == 1:
                selected_object = matching_objects[0]
            elif len(matching_objects) > 1:
                selected_object = max(matching_objects, key=lambda obj: obj['size'])

            # Draw the shape of the selected object
            if selected_object:
                for r_rel, c_rel in selected_object['coords']:
                    # Convert relative source coordinates to absolute grid coordinates
                    r_abs = r_rel + source_band['start_row']
                    c_abs = c_rel # Assuming source starts at col 0
                    
                    # Check bounds before drawing (should align with target band vertical range, but use absolute coords)
                    if target['start_row'] <= r_abs <= target['end_row'] and 0 <= c_abs < cols:
                        output_grid[r_abs, c_abs] = target_frame
                    # Need to ensure drawing happens *within* the target band space
                    # The rule implies using the source coordinates directly. Let's stick to that.
                    if 0 <= r_abs < rows and 0 <= c_abs < cols:
                         output_grid[r_abs, c_abs] = target_frame


    return output_grid.tolist()
```