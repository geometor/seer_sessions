import numpy as np
from collections import defaultdict
import itertools

"""
Transforms the input grid based on patterns within regions defined by grid lines.

1.  **Grid and Region Identification:** Identifies solid horizontal and vertical grid lines of a single non-background color. These lines partition the grid into rectangular regions.
2.  **Pattern Extraction:** For each region, extracts its content and determines its 'pattern' (the arrangement of non-background, non-grid-line colors). Empty regions have no pattern.
3.  **Transformation Rules:** Applies transformations based on the patterns and arrangement of regions:
    *   **2x2 Block - Identical Patterns:** If four adjacent regions forming a 2x2 block contain the *same* non-empty pattern, the content of the top-left region swaps with the bottom-left, and the top-right swaps with the bottom-right (vertical swaps).
    *   **2x2 Block - Distinct Patterns:** If four adjacent regions forming a 2x2 block contain four *distinct* non-empty patterns, their contents undergo a 3-cycle rotation: Top-Right moves to Bottom-Left, Bottom-Left moves to Bottom-Right, and Bottom-Right moves to Top-Right. The Top-Left region's content remains unchanged.
    *   **Group of 3 Identical Patterns:** If exactly three regions in the grid contain the *same* non-empty pattern, and they haven't been processed as part of a 2x2 block, the contents of the second and third regions (when sorted by top-left corner, row-major order) are swapped.
4.  **Execution:** Transformations are applied simultaneously to a copy of the input grid. Regions not matching these specific rules (empty regions, regions with unique patterns not part of a specific group, etc.) remain unchanged.
"""

def find_grid_lines(grid):
    """
    Finds horizontal and vertical grid lines and the single color forming them.
    A grid line is a full row or column composed of a single non-background color.
    Assumes only one such color exists based on examples.
    """
    height, width = grid.shape
    rows = []
    cols = []
    line_colors = set()

    for r in range(height):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            rows.append(r)
            line_colors.add(unique_colors[0])

    for c in range(width):
        unique_colors = np.unique(grid[:, c])
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            cols.append(c)
            line_colors.add(unique_colors[0])

    if not line_colors:
        return None, [], []
    
    # Assume only one grid line color based on provided examples
    grid_line_color = list(line_colors)[0] 

    return grid_line_color, sorted(list(set(rows))), sorted(list(set(cols)))

def define_regions(height, width, grid_rows, grid_cols):
    """
    Defines region boundaries based on grid lines.
    Returns a list of tuples: (r1, c1, r2, c2) (inclusive top-left, exclusive bottom-right).
    Also returns a mapping from (row_idx, col_idx) of regions to their coords.
    """
    regions = []
    region_grid_map = {} # Map (region_row, region_col) index to coords
    coords_to_indices = {} # Map coords to (region_row, region_col) index

    row_starts = [0] + [r + 1 for r in grid_rows]
    row_ends = [r for r in grid_rows] + [height]
    col_starts = [0] + [c + 1 for c in grid_cols]
    col_ends = [c for c in grid_cols] + [width]

    region_row_idx = 0
    for r_start, r_end in zip(row_starts, row_ends):
        if r_start >= r_end: continue
        region_col_idx = 0
        for c_start, c_end in zip(col_starts, col_ends):
            if c_start >= c_end: continue
            
            coords = (r_start, c_start, r_end, c_end)
            regions.append(coords)
            indices = (region_row_idx, region_col_idx)
            region_grid_map[indices] = coords
            coords_to_indices[coords] = indices
            
            region_col_idx += 1
        region_row_idx += 1
                
    return regions, region_grid_map, coords_to_indices

def extract_content(grid, r1, c1, r2, c2):
    """Extracts the subgrid content of a region."""
    return grid[r1:r2, c1:c2]

def get_pattern_tuple(content, background_color=0, grid_line_color=None):
    """
    Creates a hashable representation (tuple of tuples) of the pattern,
    ignoring background and grid line colors. Returns None if the region
    contains no distinct pattern pixels.
    """
    pattern_list = []
    has_pattern = False
    if content.size == 0: # Handle empty content case
        return None
        
    for r in range(content.shape[0]):
        row_list = []
        for c in range(content.shape[1]):
            pixel = content[r, c]
            if pixel != background_color and pixel != grid_line_color:
                 row_list.append(pixel)
                 has_pattern = True
            else:
                 # Represent non-pattern pixels consistently (e.g., with background)
                 # This ensures patterns are compared correctly including empty space within them.
                 row_list.append(background_color) 
        pattern_list.append(tuple(row_list))
        
    # Return None only if NO pattern pixels were found at all
    if not has_pattern:
        return None 
        
    return tuple(pattern_list)

def place_content(grid, r1, c1, r2, c2, content_to_place):
    """Places the content_to_place into the specified region of the grid."""
    if grid[r1:r2, c1:c2].shape != content_to_place.shape:
        # This shouldn't happen if regions/content are handled correctly
        print(f"Warning: Shape mismatch during placement at {r1,c1,r2,c2}. Target: {grid[r1:r2, c1:c2].shape}, Source: {content_to_place.shape}")
        # Attempt resize or handle error? For now, skip placement if shapes mismatch.
        return
    grid[r1:r2, c1:c2] = content_to_place

def transform(input_grid):
    """
    Applies transformations based on region patterns and arrangements.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    background_color = 0

    # 1. Identify Grid Structure
    grid_line_color, grid_rows, grid_cols = find_grid_lines(input_grid)
    
    if grid_line_color is None:
         # No grid lines found, assume no transformation possible based on rules
         return output_grid 

    # 2. Define Regions
    region_coords_list, region_grid_map, coords_to_indices = define_regions(height, width, grid_rows, grid_cols)

    # 3. Extract Content and Patterns
    region_data = {} # {coords: {'content': ..., 'pattern': ...}}
    pattern_groups = defaultdict(list) # {pattern: [coords1, coords2, ...]}
    for coords in region_coords_list:
        r1, c1, r2, c2 = coords
        content = extract_content(input_grid, r1, c1, r2, c2)
        pattern = get_pattern_tuple(content, background_color, grid_line_color)
        region_data[coords] = {'content': content, 'pattern': pattern}
        if pattern is not None:
            pattern_groups[pattern].append(coords)

    processed_coords = set() # Track regions already handled by a rule
    swaps_to_perform = [] # List of (coords_A, coords_B)
    rotations_to_perform = [] # List of (coords_TL, coords_TR, coords_BL, coords_BR)

    # 4. Process 2x2 Blocks
    max_region_row = max(idx[0] for idx in region_grid_map.keys()) if region_grid_map else -1
    max_region_col = max(idx[1] for idx in region_grid_map.keys()) if region_grid_map else -1

    for r in range(max_region_row):
        for c in range(max_region_col):
            idx_tl = (r, c)
            idx_tr = (r, c + 1)
            idx_bl = (r + 1, c)
            idx_br = (r + 1, c + 1)

            # Check if all four indices exist in our region map
            if all(idx in region_grid_map for idx in [idx_tl, idx_tr, idx_bl, idx_br]):
                coords_tl = region_grid_map[idx_tl]
                coords_tr = region_grid_map[idx_tr]
                coords_bl = region_grid_map[idx_bl]
                coords_br = region_grid_map[idx_br]
                
                block_coords = {coords_tl, coords_tr, coords_bl, coords_br}

                # Check if any region in this block was already processed
                if not block_coords.intersection(processed_coords):
                    p_tl = region_data[coords_tl]['pattern']
                    p_tr = region_data[coords_tr]['pattern']
                    p_bl = region_data[coords_bl]['pattern']
                    p_br = region_data[coords_br]['pattern']

                    patterns = [p_tl, p_tr, p_bl, p_br]
                    
                    # Check if all patterns are non-empty
                    if all(p is not None for p in patterns):
                        # Case 2x2 Identical
                        if len(set(patterns)) == 1:
                            swaps_to_perform.append((coords_tl, coords_bl))
                            swaps_to_perform.append((coords_tr, coords_br))
                            processed_coords.update(block_coords)
                        # Case 2x2 Distinct
                        elif len(set(patterns)) == 4:
                             rotations_to_perform.append((coords_tl, coords_tr, coords_bl, coords_br))
                             processed_coords.update(block_coords)


    # 5. Process Remaining Identical Groups (Specifically N=3 case)
    for pattern, coords_list in pattern_groups.items():
        # Filter out coords already processed by 2x2 rules
        active_coords = [c for c in coords_list if c not in processed_coords]
        
        # Case N=3 Identical
        if len(active_coords) == 3:
            # Sort by top-left corner (row, then column)
            sorted_coords = sorted(active_coords, key=lambda c: (c[0], c[1]))
            # Swap 2nd and 3rd
            swaps_to_perform.append((sorted_coords[1], sorted_coords[2]))
            processed_coords.update(active_coords) # Mark these 3 as processed


    # 6. Perform Transformations
    # Cache original content for all involved regions *before* modifying output_grid
    content_cache = {}
    regions_to_cache = set()
    for coords_A, coords_B in swaps_to_perform:
        regions_to_cache.add(coords_A)
        regions_to_cache.add(coords_B)
    for coords_TL, coords_TR, coords_BL, coords_BR in rotations_to_perform:
         regions_to_cache.add(coords_TR)
         regions_to_cache.add(coords_BL)
         regions_to_cache.add(coords_BR) # TL doesn't move, but its content might be needed if involved elsewhere? Better safe. Add all 4.
         regions_to_cache.add(coords_TL)


    for coords in regions_to_cache:
         if coords not in content_cache: # Avoid re-extracting if already cached
            content_cache[coords] = region_data[coords]['content'] # Use the originally extracted content


    # Apply swaps
    for coords_A, coords_B in swaps_to_perform:
        if coords_A in content_cache and coords_B in content_cache:
            content_A = content_cache[coords_A]
            content_B = content_cache[coords_B]
            place_content(output_grid, *coords_A, content_B)
            place_content(output_grid, *coords_B, content_A)
        else:
             print(f"Warning: Missing content cache for swap between {coords_A} and {coords_B}")

    # Apply rotations (3-cycle: TR->BL, BL->BR, BR->TR)
    for coords_TL, coords_TR, coords_BL, coords_BR in rotations_to_perform:
         # Ensure all required contents are cached
        if all(c in content_cache for c in [coords_TR, coords_BL, coords_BR]):
            content_TR = content_cache[coords_TR]
            content_BL = content_cache[coords_BL]
            content_BR = content_cache[coords_BR]
            # Perform the cycle
            place_content(output_grid, *coords_BL, content_TR) # TR content goes to BL location
            place_content(output_grid, *coords_BR, content_BL) # BL content goes to BR location
            place_content(output_grid, *coords_TR, content_BR) # BR content goes to TR location
            # TL remains unchanged: place_content(output_grid, *coords_TL, content_TL) implicitly done by copy
        else:
            print(f"Warning: Missing content cache for rotation involving {coords_TL}, {coords_TR}, {coords_BL}, {coords_BR}")


    return output_grid