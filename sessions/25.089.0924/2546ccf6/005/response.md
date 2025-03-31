```python
import numpy as np
from collections import defaultdict
import itertools

"""
Transforms the input grid based on patterns within regions defined by grid lines, applying specific rules for 2x2 blocks and groups of identical patterns.

1.  **Grid and Region Identification:** Identifies solid horizontal and vertical grid lines of a single non-background color. These lines partition the grid into rectangular regions.
2.  **Pattern Extraction:** For each region, extracts its content and determines its 'pattern' (the arrangement of non-background, non-grid-line colors, represented as a tuple of tuples). Empty regions (only background or grid line color) have a pattern of `None`.
3.  **Rule Application Strategy:**
    *   Rules are identified based on region patterns and arrangements.
    *   Transformations are scheduled first.
    *   Regions involved in a transformation are marked as 'processed' to prevent applying multiple rules to the same region.
    *   Scheduled transformations are executed simultaneously on a copy of the input grid using cached original content.
4.  **Transformation Rule 1: 2x2 Distinct Patterns:**
    *   Identifies 2x2 blocks of adjacent regions where all four regions have distinct, non-empty patterns.
    *   Schedules a 3-cycle rotation for the content of these regions: Top-Right -> Bottom-Left, Bottom-Left -> Bottom-Right, Bottom-Right -> Top-Right. The Top-Left region's content remains in place but the region is marked as processed.
5.  **Transformation Rule 2: Identical Pattern Pairs:**
    *   Groups regions with identical, non-empty patterns.
    *   For each group, considers only regions *not* already processed by Rule 1.
    *   If 2 or more unprocessed regions remain in a group, sorts them by top-left corner (row-major).
    *   Schedules content swaps between consecutive pairs (1st <-> 2nd, 3rd <-> 4th, etc.) within the sorted, unprocessed regions of that group. Marks swapped regions as processed.
6.  **Execution:** Applies all scheduled swaps and rotations to produce the final output grid. Regions not involved in any transformation remain unchanged.
"""

# --- Helper Functions ---

def find_grid_lines(grid):
    """
    Finds horizontal and vertical grid lines and the single color forming them.
    A grid line is a full row or column composed of a single non-background color.
    Assumes only one such color exists based on examples.
    Returns: grid_line_color (int or None), rows (list of int), cols (list of int)
    """
    height, width = grid.shape
    rows = []
    cols = []
    line_colors = set()

    # Find potential horizontal lines and their colors
    for r in range(height):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            rows.append(r)
            line_colors.add(unique_colors[0])

    # Find potential vertical lines and their colors
    for c in range(width):
        unique_colors = np.unique(grid[:, c])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            cols.append(c)
            line_colors.add(unique_colors[0])

    if not line_colors:
        return None, [], [] # No grid lines found

    # In this task, assume only one color forms the grid lines
    # More complex logic might be needed if multiple colors could form lines
    grid_line_color = list(line_colors)[0] 
    
    # Filter rows/cols to only include those matching the determined grid_line_color
    # This handles cases where other full lines might exist but aren't the 'grid'
    final_rows = [r for r in rows if np.all(grid[r, :] == grid_line_color)]
    final_cols = [c for c in cols if np.all(grid[:, c] == grid_line_color)]


    return grid_line_color, sorted(list(set(final_rows))), sorted(list(set(final_cols)))

def define_regions(height, width, grid_rows, grid_cols):
    """
    Defines region boundaries based on grid lines.
    Returns:
        regions_coords_list: List of tuples [(r1, c1, r2, c2), ...] (inclusive top-left, exclusive bottom-right).
        region_grid_map: Dict mapping (region_row, region_col) index to coords tuple.
        coords_to_indices: Dict mapping coords tuple back to (region_row, region_col) index.
    """
    regions_coords_list = []
    region_grid_map = {} 
    coords_to_indices = {} 

    # Define the start and end points for rows and columns based on grid lines
    row_starts = [0] + [r + 1 for r in grid_rows]
    row_ends = [r for r in grid_rows] + [height]
    col_starts = [0] + [c + 1 for c in grid_cols]
    col_ends = [c for c in grid_cols] + [width]

    region_row_idx = 0
    for r_start, r_end in zip(row_starts, row_ends):
        # Skip if the region would have zero height (e.g., adjacent grid lines)
        if r_start >= r_end: continue 
        region_col_idx = 0
        for c_start, c_end in zip(col_starts, col_ends):
            # Skip if the region would have zero width
            if c_start >= c_end: continue 
            
            coords = (r_start, c_start, r_end, c_end)
            regions_coords_list.append(coords)
            
            indices = (region_row_idx, region_col_idx)
            region_grid_map[indices] = coords
            coords_to_indices[coords] = indices
            
            region_col_idx += 1
        region_row_idx += 1
                
    return regions_coords_list, region_grid_map, coords_to_indices

def extract_content(grid, r1, c1, r2, c2):
    """Extracts the subgrid content of a region."""
    return grid[r1:r2, c1:c2]

def get_pattern_tuple(content, background_color=0, grid_line_color=None):
    """
    Creates a hashable representation (tuple of tuples) of the pattern within content,
    ignoring background and grid line colors by replacing them with background_color.
    Returns None if the region contains no distinct pattern pixels (only background/grid_line_color).
    """
    if content is None or content.size == 0:
        return None
        
    pattern_list = []
    has_pattern_pixel = False
    
    # Iterate through each pixel of the content subgrid
    for r in range(content.shape[0]):
        row_list = []
        for c in range(content.shape[1]):
            pixel = content[r, c]
            # Check if the pixel is a pattern pixel (not background, not grid line)
            if pixel != background_color and pixel != grid_line_color:
                 row_list.append(pixel)
                 has_pattern_pixel = True # Mark that we found at least one pattern pixel
            else:
                 # Replace background/grid line pixels with background color for pattern representation
                 row_list.append(background_color) 
        pattern_list.append(tuple(row_list))
        
    # Only return a pattern if it contained at least one non-background, non-grid-line pixel
    if not has_pattern_pixel:
        return None 
        
    return tuple(pattern_list)

def place_content(grid, r1, c1, r2, c2, content_to_place):
    """Places the content_to_place into the specified region of the grid."""
    # Check for shape mismatch to prevent errors
    target_shape = grid[r1:r2, c1:c2].shape
    source_shape = content_to_place.shape
    if target_shape != source_shape:
        print(f"Error: Shape mismatch during placement at ({r1}:{r2}, {c1}:{c2}). Target: {target_shape}, Source: {source_shape}")
        # Optionally raise an error or handle differently
        return # Skip placement if shapes don't match
    grid[r1:r2, c1:c2] = content_to_place

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies transformations based on region patterns and arrangements following the described rules.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    background_color = 0

    # 1. Identify Grid Structure
    grid_line_color, grid_rows, grid_cols = find_grid_lines(input_grid)
    
    # If no grid lines, no regions defined by lines, so return the original grid
    if grid_line_color is None:
         return output_grid 

    # 2. Define Regions
    region_coords_list, region_grid_map, coords_to_indices = define_regions(height, width, grid_rows, grid_cols)

    # 3. Extract Content and Patterns for each region
    region_data = {} # Stores data per region: {coords: {'content': ndarray, 'pattern': tuple/None, 'indices': (r_idx, c_idx)}}
    pattern_groups = defaultdict(list) # Groups coords by pattern: {pattern_tuple: [coords1, coords2, ...]}
    
    for coords in region_coords_list:
        r1, c1, r2, c2 = coords
        content = extract_content(input_grid, r1, c1, r2, c2)
        pattern = get_pattern_tuple(content, background_color, grid_line_color)
        indices = coords_to_indices[coords]
        
        region_data[coords] = {'content': content, 'pattern': pattern, 'indices': indices}
        
        # Add to pattern group only if it has a non-empty pattern
        if pattern is not None:
            pattern_groups[pattern].append(coords)

    # --- Identify Transformations to Schedule ---
    processed_coords = set() # Track region coordinates already part of a transformation
    swaps_to_schedule = [] # List of pairs of coords to swap: [ (coords_A, coords_B), ... ]
    rotations_to_schedule = [] # List of 4-tuples for 2x2 distinct rotation: [ (tl, tr, bl, br), ... ]

    # 4. Schedule Rule 1: 2x2 Distinct Patterns Rotation
    max_region_row = max(idx[0] for idx in region_grid_map.keys()) if region_grid_map else -1
    max_region_col = max(idx[1] for idx in region_grid_map.keys()) if region_grid_map else -1

    # Iterate through top-left corners of potential 2x2 blocks
    for r_idx in range(max_region_row):
        for c_idx in range(max_region_col):
            idx_tl = (r_idx, c_idx)
            idx_tr = (r_idx, c_idx + 1)
            idx_bl = (r_idx + 1, c_idx)
            idx_br = (r_idx + 1, c_idx + 1)

            # Check if all four region indices form a valid 2x2 block in the region grid
            if all(idx in region_grid_map for idx in [idx_tl, idx_tr, idx_bl, idx_br]):
                coords_tl = region_grid_map[idx_tl]
                coords_tr = region_grid_map[idx_tr]
                coords_bl = region_grid_map[idx_bl]
                coords_br = region_grid_map[idx_br]
                
                block_coords_set = {coords_tl, coords_tr, coords_bl, coords_br}

                # Check if any region in this block has already been processed by another rule
                if not block_coords_set.intersection(processed_coords):
                    # Get patterns for the four regions
                    p_tl = region_data[coords_tl]['pattern']
                    p_tr = region_data[coords_tr]['pattern']
                    p_bl = region_data[coords_bl]['pattern']
                    p_br = region_data[coords_br]['pattern']

                    patterns_in_block = [p_tl, p_tr, p_bl, p_br]
                    
                    # Rule condition: All four patterns must be non-empty (not None)
                    if all(p is not None for p in patterns_in_block):
                        # Rule condition: All four patterns must be distinct
                        if len(set(patterns_in_block)) == 4:
                             # Schedule the rotation
                             rotations_to_schedule.append((coords_tl, coords_tr, coords_bl, coords_br))
                             # Mark these regions as processed so they aren't used in Rule 2
                             processed_coords.update(block_coords_set)


    # 5. Schedule Rule 2: Identical Pattern Swaps (Pairs)
    for pattern, coords_list in pattern_groups.items():
        # Consider only regions *not* already processed by the 2x2 rule
        unprocessed_coords_in_group = [c for c in coords_list if c not in processed_coords]
        
        # Rule condition: Need at least 2 unprocessed regions with the same pattern
        if len(unprocessed_coords_in_group) >= 2:
            # Sort these regions by their top-left corner (row, then column) for consistent pairing
            sorted_unprocessed_coords = sorted(unprocessed_coords_in_group, key=lambda c: (c[0], c[1]))
            
            # Iterate through pairs (0,1), (2,3), ...
            for i in range(0, len(sorted_unprocessed_coords) // 2 * 2, 2):
                coords_A = sorted_unprocessed_coords[i]
                coords_B = sorted_unprocessed_coords[i+1]
                # Schedule the swap
                swaps_to_schedule.append((coords_A, coords_B))
                # Mark these two regions as processed
                processed_coords.add(coords_A)
                processed_coords.add(coords_B)


    # --- Execute Scheduled Transformations ---

    # 6. Cache original content for all regions involved in any transformation
    # This ensures we use the state from the *input* grid for all operations
    content_cache = {}
    regions_to_cache = set()
    
    # Gather regions involved in swaps
    for coords_A, coords_B in swaps_to_schedule:
        regions_to_cache.add(coords_A)
        regions_to_cache.add(coords_B)
        
    # Gather regions involved in rotations (need original content of the 3 moving pieces)
    for coords_TL, coords_TR, coords_BL, coords_BR in rotations_to_schedule:
         regions_to_cache.add(coords_TR)
         regions_to_cache.add(coords_BL)
         regions_to_cache.add(coords_BR)
         # Note: coords_TL isn't strictly needed for the rotation itself, 
         # but caching it doesn't hurt and simplifies logic slightly.

    # Populate the cache using the original region_data
    for coords in regions_to_cache:
         if coords in region_data: # Check if coords are valid
            content_cache[coords] = region_data[coords]['content']
         else:
             print(f"Warning: Attempting to cache content for unknown coords: {coords}")


    # 7. Apply Swaps to the output_grid using cached content
    for coords_A, coords_B in swaps_to_schedule:
        # Ensure both regions' original content was successfully cached
        if coords_A in content_cache and coords_B in content_cache:
            content_A_original = content_cache[coords_A]
            content_B_original = content_cache[coords_B]
            
            # Perform swap on output grid
            place_content(output_grid, *coords_A, content_B_original)
            place_content(output_grid, *coords_B, content_A_original)
        else:
             print(f"Warning: Could not perform swap. Missing original content for {coords_A} or {coords_B}")

    # 8. Apply Rotations to the output_grid using cached content
    # Rotation is a 3-cycle: TR -> BL, BL -> BR, BR -> TR
    for coords_TL, coords_TR, coords_BL, coords_BR in rotations_to_schedule:
         # Ensure the 3 moving pieces' original content was cached
        if all(c in content_cache for c in [coords_TR, coords_BL, coords_BR]):
            content_TR_original = content_cache[coords_TR]
            content_BL_original = content_cache[coords_BL]
            content_BR_original = content_cache[coords_BR]
            
            # Perform the cyclic placement on the output grid
            place_content(output_grid, *coords_BL, content_TR_original) # TR content goes to BL location
            place_content(output_grid, *coords_BR, content_BL_original) # BL content goes to BR location
            place_content(output_grid, *coords_TR, content_BR_original) # BR content goes to TR location
            # TL location remains unchanged (already copied in output_grid initialization)
        else:
            print(f"Warning: Could not perform rotation. Missing original content for one of {coords_TR}, {coords_BL}, {coords_BR}")

    # 9. Return the final state of the output grid
    return output_grid
```