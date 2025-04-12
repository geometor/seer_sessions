```python
import numpy as np
from collections import Counter, deque
from typing import List, Dict, Tuple, Set, Optional

"""
Transforms an input grid based on rules derived from a key area outside a main frame.

The transformation involves:
1. Finding a hollow rectangular frame of gray (5) pixels.
2. Analyzing the area outside the frame (KeyArea) to find:
    a. Solid blocks of unique 'SourceColor'.
    b. Template blocks composed of a 'TargetColor' and the 'BackgroundColor'.
    c. Adjacency between Solid blocks and Template blocks to establish:
        i. Mappings: SourceColor -> TargetColor
        ii. Template Shapes: The array shape/content associated with each SourceColor.
    d. The invariant 'BackgroundColor' (most frequent outside color not part of the frame or mapping pairs).
3. Initializing an output grid based on the frame's dimensions, filled with the BackgroundColor.
4. Copying the gray frame pixels to the output grid.
5. Finding instances of SourceColor blocks within the input frame.
6. For each Source Block Instance found inside the frame:
    a. Retrieve its associated Template Shape and TargetColor using the mapping.
    b. "Paint" the Template Shape onto the output grid at the Source Block Instance's top-left position, replacing the template's original TargetColor pixels with the mapped TargetColor and the template's BackgroundColor pixels with the BackgroundColor.
7. Returning the final output grid.
"""

# --- Helper Functions ---

def find_frame_bbox(grid_np: np.ndarray, frame_color: int = 5) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the bounding box coords (min_r, min_c, max_r, max_c) of the largest hollow rectangle made of frame_color.
    Returns None if no valid frame is found.
    """
    coords = np.argwhere(grid_np == frame_color)
    if coords.size == 0:
        return None
        
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)

    # Check if frame is too small to be hollow
    if r_max < r_min + 2 or c_max < c_min + 2:
         # Handle thin "frames" - are they allowed? Assume requires hollow for now.
         # Basic check: all coords must be on border
         on_border = (coords[:, 0] == r_min) | (coords[:, 0] == r_max) | \
                     (coords[:, 1] == c_min) | (coords[:, 1] == c_max)
         if np.all(on_border):
             # Check if it's just a line or corner, needs at least 4 pixels for a minimal frame?
             # A simple line might be ambiguous. For simplicity, require a hollow potential.
             # Let's assume a valid frame must have potential for interior (size >= 3x3)
             # Or adjust if examples show line frames. Sticking to hollow assumption.
             if r_max >= r_min + 2 and c_max >= c_min + 2: # Potential interior
                 pass # Check below
             else:
                 return None # Too small to be hollow

    # Verify all frame_color pixels are on the border
    on_border_check = (coords[:, 0] == r_min) | (coords[:, 0] == r_max) | \
                      (coords[:, 1] == c_min) | (coords[:, 1] == c_max)
    if not np.all(on_border_check):
        return None # Pixels with frame color exist *not* on the border defined by min/max

    # Verify the inside is not the frame color (ensure it's hollow)
    inner_slice = grid_np[r_min + 1:r_max, c_min + 1:c_max]
    if np.any(inner_slice == frame_color):
        return None # Frame color found inside, not a simple hollow frame

    return (r_min, c_min, r_max, c_max)


def find_contiguous_blocks(grid_np: np.ndarray, 
                           allowed_colors: Set[int],
                           search_bounds: Optional[Tuple[int, int, int, int]] = None,
                           start_coord: Optional[Tuple[int, int]] = None,
                           ignore_mask: Optional[np.ndarray] = None) -> List[Dict]:
    """
    Finds contiguous blocks of any single color within allowed_colors, optionally within bounds.
    
    Args:
        grid_np: The grid to search.
        allowed_colors: Set of colors to form blocks.
        search_bounds: Optional (r0, c0, r1, c1) exclusive bounds for search.
        start_coord: If provided, only find the block containing this coordinate.
        ignore_mask: Optional boolean array where True means ignore this cell.

    Returns:
        List of dictionaries, each: {'color', 'coords', 'r_min', 'c_min', 'r_max', 'c_max'}
    """
    rows, cols = grid_np.shape
    if search_bounds:
        r_start, c_start, r_end, c_end = search_bounds
    else:
        r_start, c_start, r_end, c_end = 0, 0, rows, cols

    visited = np.zeros_like(grid_np, dtype=bool)
    if ignore_mask is not None:
        visited |= ignore_mask # Pre-mark ignored cells as visited

    blocks = []
    
    search_queue = deque()
    if start_coord:
        # Check if start_coord is valid and within bounds
        sr, sc = start_coord
        if r_start <= sr < r_end and c_start <= sc < c_end and not visited[sr, sc]:
             search_queue.append(start_coord)
    else:
        # Add all valid starting points within bounds
        for r in range(r_start, r_end):
             for c in range(c_start, c_end):
                 if not visited[r, c] and grid_np[r, c] in allowed_colors:
                     search_queue.append((r, c))

    processed_starts = set() # Avoid redundant BFS starts if queue has duplicates initially

    while search_queue:
        r_init, c_init = search_queue.popleft()
        
        if visited[r_init, c_init] or (r_init, c_init) in processed_starts:
            continue
            
        color = grid_np[r_init, c_init]
        if color not in allowed_colors: # Should not happen if queue is built correctly
            continue

        processed_starts.add((r_init, c_init)) # Mark this starting cell as processed for queue

        block_coords = set()
        q = deque([(r_init, c_init)])
        visited[r_init, c_init] = True
        r_min_blk, c_min_blk = r_init, c_init
        r_max_blk, c_max_blk = r_init, c_init
        
        while q:
            r, c = q.popleft()
            block_coords.add((r, c))
            r_min_blk, c_min_blk = min(r_min_blk, r), min(c_min_blk, c)
            r_max_blk, c_max_blk = max(r_max_blk, r), max(c_max_blk, c)

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check grid bounds and search bounds
                if 0 <= nr < rows and 0 <= nc < cols and \
                   r_start <= nr < r_end and c_start <= nc < c_end and \
                   not visited[nr, nc] and grid_np[nr, nc] == color:
                    visited[nr, nc] = True
                    q.append((nr, nc))

        blocks.append({
            'color': color, 
            'coords': block_coords,
            'r_min': r_min_blk, 'c_min': c_min_blk, 
            'r_max': r_max_blk, 'c_max': c_max_blk
        })
        
        # If we were searching for a specific start coord's block, we found it.
        if start_coord:
            break 
                 
    return blocks


def analyze_key_area(grid_np: np.ndarray, frame_bbox: Tuple[int, int, int, int], frame_color: int) -> Optional[Tuple[Dict[int, int], int, Dict[int, np.ndarray]]]:
    """
    Analyzes the area outside the frame to find mappings, background, and templates.

    Returns:
        Tuple (mappings, background_color, templates) or None if analysis fails.
        mappings: {source_color: target_color}
        background_color: int
        templates: {source_color: template_array}
    """
    rows, cols = grid_np.shape
    r_min_f, c_min_f, r_max_f, c_max_f = frame_bbox
    
    # --- Create Mask for Key Area (Outside Frame) ---
    key_area_mask = np.ones_like(grid_np, dtype=bool)
    key_area_mask[r_min_f:r_max_f + 1, c_min_f:c_max_f + 1] = False
    
    # --- Initial Background Color Guess ---
    outside_colors_counter = Counter()
    key_area_coords = np.argwhere(key_area_mask)
    for r, c in key_area_coords:
        color = grid_np[r, c]
        if color != frame_color: # Should always be true if mask is correct
            outside_colors_counter[color] += 1
            
    if not outside_colors_counter:
        print("Warning: No non-frame colors found outside the frame.")
        return None # Cannot determine rules

    # Most frequent color outside is potential background
    # Sort by frequency (desc), then color value (asc) for tie-breaking
    sorted_outside_colors = sorted(outside_colors_counter.items(), key=lambda item: (-item[1], item[0]))
    potential_background = sorted_outside_colors[0][0]

    # --- Find Components (Solid & Template Candidates) Outside Frame ---
    visited_key = np.zeros_like(grid_np, dtype=bool)
    visited_key[~key_area_mask] = True # Mark frame and inside as visited

    solid_blocks = []
    template_candidates = [] # Store potential template blocks before background is finalized

    for r_init, c_init in key_area_coords:
         if not visited_key[r_init, c_init]:
            component_coords = set()
            colors_in_component = set()
            q = deque([(r_init, c_init)])
            visited_key[r_init, c_init] = True
            r_min_comp, c_min_comp = r_init, c_init
            r_max_comp, c_max_comp = r_init, c_init

            while q:
                r, c = q.popleft()
                color = grid_np[r, c]
                # Check if color is frame color - should not happen if mask is right
                if color == frame_color: continue 
                
                colors_in_component.add(color)
                component_coords.add((r,c))
                r_min_comp, c_min_comp = min(r_min_comp, r), min(c_min_comp, c)
                r_max_comp, c_max_comp = max(r_max_comp, r), max(c_max_comp, c)

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    # Check bounds and if it's in the key area (i.e., not visited)
                    if 0 <= nr < rows and 0 <= nc < cols and not visited_key[nr, nc]:
                        # Connect components regardless of color initially
                        visited_key[nr, nc] = True
                        q.append((nr, nc))

            # --- Categorize Component ---
            non_background_candidates = colors_in_component - {potential_background}
            
            if len(non_background_candidates) == 1:
                single_color = list(non_background_candidates)[0]
                if len(colors_in_component) == 1: # Solid Block
                    solid_blocks.append({
                        'color': single_color, 'coords': component_coords,
                        'r_min': r_min_comp, 'c_min': c_min_comp,
                        'r_max': r_max_comp, 'c_max': c_max_comp
                    })
                elif len(colors_in_component) == 2 and potential_background in colors_in_component:
                     # Potential Template Block
                     template_arr = grid_np[r_min_comp:r_max_comp+1, c_min_comp:c_max_comp+1].copy()
                     template_candidates.append({
                         'target_color': single_color, 
                         'potential_bg': potential_background,
                         'coords': component_coords,
                         'r_min': r_min_comp, 'c_min': c_min_comp,
                         'r_max': r_max_comp, 'c_max': c_max_comp,
                         'array': template_arr
                     })
            # else: Mixed block or just background - ignore for mapping

    # --- Determine Final Background & Mappings ---
    solid_colors = {b['color'] for b in solid_blocks}
    target_colors = {b['target_color'] for b in template_candidates}
    possible_mapping_colors = solid_colors | target_colors

    background_color = -1
    for color, count in sorted_outside_colors:
        if color not in possible_mapping_colors:
             background_color = color
             break
    if background_color == -1:
         # Fallback: Use the initial potential background if all colors were involved in pairs
         background_color = potential_background
         # print(f"Warning: All outside colors involved in potential pairs. Using initial guess {background_color} as background.")

    # Filter template candidates based on the final background color
    valid_template_blocks = [
        tc for tc in template_candidates if tc['potential_bg'] == background_color
    ]
    
    # Find mappings by adjacency
    mappings = {}
    templates = {}
    mapped_target_colors = set() # Track target colors already used in a mapping

    for sb in solid_blocks:
        source_color = sb['color']
        if source_color in mappings: continue 

        best_match_template = None
        
        for tb in valid_template_blocks:
            target_color = tb['target_color']
            # Ensure this target color hasn't been mapped *to* already
            if target_color in mapped_target_colors: continue 

            # Check adjacency
            is_adjacent = False
            for r_s, c_s in sb['coords']:
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                     nr, nc = r_s + dr, c_s + dc
                     if (nr, nc) in tb['coords']:
                         is_adjacent = True
                         break
                 if is_adjacent: break
            
            if is_adjacent:
                # Found a potential match. Since a source might be adjacent to multiple
                # things, maybe store first match? Or require unique pairings?
                # Assume first adjacent match is correct for now.
                best_match_template = tb
                break 

        if best_match_template:
            target_color = best_match_template['target_color']
            mappings[source_color] = target_color
            templates[source_color] = best_match_template['array']
            mapped_target_colors.add(target_color) # Mark target as used

    if not mappings:
        # print("Warning: No mappings found between solid and template blocks.")
        return None # Cannot proceed

    return mappings, background_color, templates


# --- Main Transformation Function ---

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the frame-key-template transformation.
    """
    input_np = np.array(input_grid, dtype=int)
    frame_color = 5

    # --- Step 1: Find the Frame ---
    frame_bbox = find_frame_bbox(input_np, frame_color)
    if frame_bbox is None:
        # print("No valid frame found. Returning input grid.")
        return input_grid
    r_min_f, c_min_f, r_max_f, c_max_f = frame_bbox

    # --- Step 2: Analyze Key Area ---
    analysis_result = analyze_key_area(input_np, frame_bbox, frame_color)
    if analysis_result is None:
         # print("Failed to analyze key area. Returning input grid.")
         return input_grid # Or handle error differently
    mappings, background_color, templates = analysis_result
    
    if not mappings or not templates:
        # print("Analysis incomplete (no mappings or templates). Returning input grid.")
        return input_grid

    # --- Step 3: Initialize Output Grid ---
    output_h = r_max_f - r_min_f + 1
    output_w = c_max_f - c_min_f + 1
    output_np = np.full((output_h, output_w), background_color, dtype=int)

    # --- Step 4: Copy Frame ---
    # Get coordinates relative to the frame bounding box start
    frame_coords_relative = np.argwhere(input_np[r_min_f:r_max_f+1, c_min_f:c_max_f+1] == frame_color)
    for r_rel, c_rel in frame_coords_relative:
        output_np[r_rel, c_rel] = frame_color

    # --- Step 5: Transform Instances Inside Frame ---
    source_colors = set(mappings.keys())
    # Define search bounds for inside the frame (exclusive of border)
    inner_bounds = (r_min_f + 1, c_min_f + 1, r_max_f, c_max_f)
    # Create ignore mask for frame pixels within the output grid dimensions
    output_ignore_mask = (output_np == frame_color)

    # Find all source blocks within the inner bounds
    source_instances = find_contiguous_blocks(input_np, source_colors, search_bounds=inner_bounds)

    processed_output_cells = output_ignore_mask.copy() # Track painted cells

    for instance in source_instances:
        source_color = instance['color']
        # Use the top-left corner of the block instance for placement
        r_abs = instance['r_min']
        c_abs = instance['c_min']
        
        if source_color in templates:
            template_shape = templates[source_color]
            target_color = mappings[source_color]
            t_h, t_w = template_shape.shape

            # Calculate placement coords relative to output grid
            r_rel = r_abs - r_min_f
            c_rel = c_abs - c_min_f

            # Apply the template
            for r_t in range(t_h):
                for c_t in range(t_w):
                    out_r = r_rel + r_t
                    out_c = c_rel + c_t

                    # Check bounds of output grid
                    if 0 <= out_r < output_h and 0 <= out_c < output_w:
                        # Check if this cell was already painted or is frame
                        if processed_output_cells[out_r, out_c]:
                            continue

                        template_pixel_color = template_shape[r_t, c_t]
                        output_color = -1 # Undefined

                        # Determine output color based on template content
                        # Important: Compare template_pixel_color with the TARGET color 
                        # found *in the template* during analysis, not the mapped target color.
                        # However, our analyze_key_area stores the template array directly.
                        # So, we need to know which color *in the template array* corresponds to the TARGET.
                        # Assumption: the template contains only background_color and the target_color from the mapping.
                        if template_pixel_color == target_color:
                             output_color = target_color
                        elif template_pixel_color == background_color:
                             output_color = background_color
                        # Else: template contains unexpected color? Skip painting this pixel.
                        
                        if output_color != -1:
                             output_np[out_r, out_c] = output_color
                             processed_output_cells[out_r, out_c] = True # Mark as painted
        #else: No template found for this source color, skipped.


    # --- Step 6: Return Output ---
    output_grid = output_np.tolist()
    return output_grid
```