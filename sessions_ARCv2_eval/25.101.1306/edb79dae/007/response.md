```python
import numpy as np
from collections import Counter, deque
from typing import List, Dict, Tuple, Set, Optional

"""
Transforms an input grid based on rules derived from a key area outside a main frame.

The process involves:
1. Finding a hollow rectangular frame of gray (5) pixels.
2. Analyzing the area outside the frame (KeyArea) to find:
    a. Source Shapes: Solid blocks of a single 'SourceColor'.
    b. Output Shapes: Patterned blocks composed of a 'TargetColor' and the 'BackgroundColor'.
    c. Adjacency between Source Shapes and Output Shapes to establish:
        i. Mappings: SourceColor -> TargetColor
        ii. Templates: The array shape/content of the Output Shape associated with each SourceColor.
    d. The invariant 'BackgroundColor' (most frequent outside color not part of the frame or mapping pairs).
3. Initializing an output grid based on the frame's dimensions, filled with the BackgroundColor.
4. Copying the gray frame pixels to the output grid.
5. Finding instances of SourceColor blocks within the input frame (Source Instances).
6. For each Source Instance found inside the frame:
    a. Retrieve its associated Template (Output Shape array) and TargetColor using the mapping.
    b. "Paint" the Template onto the output grid at the Source Instance's top-left position, using the TargetColor and BackgroundColor found within the template.
7. Returning the final output grid.
"""

# --- Helper Functions ---

def find_frame_bbox(grid_np: np.ndarray, frame_color: int = 5) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the bounding box coords (min_r, min_c, max_r, max_c) of the largest hollow rectangle made of frame_color.
    Returns None if no valid frame is found (requires potential for hollow interior, >= 3x3).
    """
    coords = np.argwhere(grid_np == frame_color)
    if coords.size < 4: # Need at least 4 pixels for the smallest possible hollow frame (corners)
        return None
        
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)

    # Check if frame is too small to be hollow
    if r_max < r_min + 2 or c_max < c_min + 2: 
         return None # Too small to have a distinct interior

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
                           search_mask: Optional[np.ndarray] = None, # Mask indicating where to search (True = search here)
                           start_coord: Optional[Tuple[int, int]] = None
                           ) -> List[Dict]:
    """
    Finds contiguous blocks of any single color within allowed_colors, searching only where search_mask is True.
    
    Args:
        grid_np: The grid to search.
        allowed_colors: Set of colors to form blocks.
        search_mask: Boolean array where True indicates searchable cells. If None, search entire grid.
        start_coord: If provided, only find the block containing this coordinate.

    Returns:
        List of dictionaries, each: {'color', 'coords', 'r_min', 'c_min', 'r_max', 'c_max'}
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    if search_mask is not None:
        visited[~search_mask] = True # Mark non-searchable areas as visited
    else:
        # If no mask, create a mask allowing search everywhere
        search_mask = np.ones_like(grid_np, dtype=bool) 

    blocks = []
    
    q_bfs = deque()

    if start_coord:
        sr, sc = start_coord
        # Check if start_coord is valid and searchable
        if 0 <= sr < rows and 0 <= sc < cols and search_mask[sr, sc] and grid_np[sr,sc] in allowed_colors:
             if not visited[sr, sc]:
                 q_bfs.append(start_coord)
                 visited[sr, sc] = True # Mark start coord as visited for BFS queue
        else:
             return [] # Start coord invalid or not allowed color/location
    else:
        # Add all valid starting points within the search mask
        search_coords = np.argwhere(search_mask)
        for r_init, c_init in search_coords:
             if not visited[r_init, c_init] and grid_np[r_init, c_init] in allowed_colors:
                 q_bfs.append((r_init, c_init))
                 visited[r_init, c_init] = True # Mark as visited for BFS queue

    processed_starts = set() # Track actual BFS roots processed

    while q_bfs:
        r_init, c_init = q_bfs.popleft()
        
        # Double check if visited (might happen if added multiple times before processing)
        # Also check if this specific start was already processed by a previous BFS run
        if (r_init, c_init) in processed_starts:
             continue
             
        # Perform BFS for the block starting from (r_init, c_init)
        color = grid_np[r_init, c_init]
        block_coords = set()
        q_block = deque([(r_init, c_init)])
        # Mark the initial cell as the start of this BFS run
        processed_starts.add((r_init, c_init)) 
        
        r_min_blk, c_min_blk = r_init, c_init
        r_max_blk, c_max_blk = r_init, c_init
        
        while q_block:
            r, c = q_block.popleft()
            block_coords.add((r, c))
            r_min_blk, c_min_blk = min(r_min_blk, r), min(c_min_blk, c)
            r_max_blk, c_max_blk = max(r_max_blk, r), max(c_max_blk, c)

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check grid bounds and if the neighbor is searchable, same color, and not visited by THIS BFS run yet
                if 0 <= nr < rows and 0 <= nc < cols and \
                   search_mask[nr, nc] and \
                   grid_np[nr, nc] == color and \
                   (nr, nc) not in processed_starts and \
                   (nr, nc) not in block_coords : # Check block_coords avoids adding back to q_block within same BFS
                    
                    # Check if already visited by the main BFS queue preparation - if so, mark as processed start
                    if visited[nr,nc]:
                         processed_starts.add((nr,nc))
                    else:
                         # Mark as visited for main BFS queue and add to this block's BFS
                         visited[nr, nc] = True 
                         q_block.append((nr, nc))
                         # also mark as processed start to prevent future BFS runs from here
                         processed_starts.add((nr,nc)) 
                         

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
    key_area_mask = np.ones(grid_np.shape, dtype=bool)
    key_area_mask[r_min_f:r_max_f + 1, c_min_f:c_max_f + 1] = False
    
    if not np.any(key_area_mask): return None # No key area exists

    # --- Initial Background Color Guess ---
    outside_colors_counter = Counter()
    key_area_coords = np.argwhere(key_area_mask)
    for r, c in key_area_coords:
        outside_colors_counter[grid_np[r, c]] += 1
            
    if not outside_colors_counter: return None

    sorted_outside_colors = sorted(outside_colors_counter.items(), key=lambda item: (-item[1], item[0]))
    potential_background = sorted_outside_colors[0][0]

    # --- Find Components (Solid & Pattern Candidates) Outside Frame ---
    visited_key = np.zeros_like(grid_np, dtype=bool)
    visited_key[~key_area_mask] = True # Mark frame and inside as visited

    source_shapes = [] # Solid blocks
    output_shape_candidates = [] # Pattern blocks (T + potential BG)

    key_area_q = deque([(r,c) for r, c in key_area_coords if not visited_key[r,c]])
    processed_starts_key = set()

    while key_area_q:
         r_init, c_init = key_area_q.popleft()
         
         if visited_key[r_init, c_init] or (r_init, c_init) in processed_starts_key:
             continue

         component_coords = set()
         colors_in_component = set()
         q_comp = deque([(r_init, c_init)])
         visited_key[r_init, c_init] = True
         processed_starts_key.add((r_init, c_init))
         
         r_min_comp, c_min_comp = r_init, c_init
         r_max_comp, c_max_comp = r_init, c_init

         while q_comp:
             r, c = q_comp.popleft()
             color = grid_np[r, c]
             
             colors_in_component.add(color)
             component_coords.add((r,c))
             r_min_comp, c_min_comp = min(r_min_comp, r), min(c_min_comp, c)
             r_max_comp, c_max_comp = max(r_max_comp, r), max(c_max_comp, c)

             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r + dr, c + dc
                 # Check bounds and if it's in the key area and not visited
                 if 0 <= nr < rows and 0 <= nc < cols and key_area_mask[nr, nc] and not visited_key[nr, nc]:
                     visited_key[nr, nc] = True
                     processed_starts_key.add((nr, nc)) # Mark as processed start too
                     q_comp.append((nr, nc))

         # --- Categorize Component ---
         if len(colors_in_component) == 1:
             color_s = list(colors_in_component)[0]
             if color_s != potential_background:
                 source_shapes.append({
                     'color': color_s, 'coords': component_coords,
                     'r_min': r_min_comp, 'c_min': c_min_comp, 'r_max': r_max_comp, 'c_max': c_max_comp
                 })
         elif len(colors_in_component) == 2 and potential_background in colors_in_component:
             color_t = list(colors_in_component - {potential_background})[0]
             pattern_arr = grid_np[r_min_comp:r_max_comp+1, c_min_comp:c_max_comp+1].copy()
             output_shape_candidates.append({
                  'target_color': color_t, 
                  'potential_bg': potential_background,
                  'coords': component_coords,
                  'r_min': r_min_comp, 'c_min': c_min_comp, 'r_max': r_max_comp, 'c_max': c_max_comp,
                  'array': pattern_arr
              })

    # --- Determine Final Background & Mappings ---
    source_colors = {s['color'] for s in source_shapes}
    target_colors = {o['target_color'] for o in output_shape_candidates}
    
    background_color = -1
    for color, count in sorted_outside_colors:
        if color not in source_colors and color not in target_colors:
            background_color = color
            break
            
    if background_color == -1: 
        background_color = potential_background 

    # Filter output shapes based on final background
    valid_output_shapes = [o for o in output_shape_candidates if o['potential_bg'] == background_color]
    
    mappings = {}
    templates = {}
    used_output_shapes_indices = set()

    for ss in source_shapes:
        source_color = ss['color']
        if source_color in mappings: continue
        
        adjacent_output_shape_idx = -1
        for idx, os in enumerate(valid_output_shapes):
             if idx in used_output_shapes_indices: continue # Skip if already paired

             # Check adjacency
             is_adjacent = False
             for r_s, c_s in ss['coords']:
                  for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                      nr, nc = r_s + dr, c_s + dc
                      if (nr, nc) in os['coords']:
                          is_adjacent = True
                          break
                  if is_adjacent: break
             
             if is_adjacent:
                  adjacent_output_shape_idx = idx
                  break 

        if adjacent_output_shape_idx != -1:
            matched_os = valid_output_shapes[adjacent_output_shape_idx]
            target_color = matched_os['target_color']
            
            # Check if this target color is already mapped to by another source
            already_mapped_to = False
            for mapped_target in mappings.values():
                 if mapped_target == target_color:
                     already_mapped_to = True
                     break

            # Only create mapping if target is not already used and shape index not used
            if not already_mapped_to:
                mappings[source_color] = target_color
                templates[source_color] = matched_os['array']
                used_output_shapes_indices.add(adjacent_output_shape_idx)
            # else: print(f"Conflict: Target color {target_color} already mapped to, skipping pair for source {source_color}")

    if not mappings: return None

    return mappings, background_color, templates

# --- Main Transformation Function ---

def transform(input_grid: List[List[int]]) -> List[List[int]]:  
    """
    Transforms the input grid using frame, key area analysis, and template painting.
    """
    input_np = np.array(input_grid, dtype=int)
    frame_color = 5

    # --- Step 1: Find Frame ---
    frame_bbox = find_frame_bbox(input_np, frame_color)
    if frame_bbox is None:
        return input_grid # No valid frame found
    r_min_f, c_min_f, r_max_f, c_max_f = frame_bbox

    # --- Step 2: Analyze Key Area ---
    analysis_result = analyze_key_area(input_np, frame_bbox, frame_color)
    if analysis_result is None:
         return input_grid # Analysis failed
    mappings, background_color, templates = analysis_result
    
    if not mappings or not templates:
        return input_grid # Analysis incomplete

    # --- Step 3: Initialize Output Grid ---
    output_h = r_max_f - r_min_f + 1
    output_w = c_max_f - c_min_f + 1
    output_np = np.full((output_h, output_w), background_color, dtype=int)

    # --- Step 4: Copy Frame ---
    frame_coords_relative = np.argwhere(input_np[r_min_f:r_max_f+1, c_min_f:c_max_f+1] == frame_color)
    for r_rel, c_rel in frame_coords_relative:
        # Check bounds just in case, though relative coords should be correct
        if 0 <= r_rel < output_h and 0 <= c_rel < output_w:
             output_np[r_rel, c_rel] = frame_color

    # --- Step 5: Transform Source Instances ---
    source_colors = set(mappings.keys())
    # Define search mask for inside the frame (exclusive of border)
    inner_mask = np.zeros_like(input_np, dtype=bool)
    if r_max_f > r_min_f + 1 and c_max_f > c_min_f + 1: # Check if inner area exists
        inner_mask[r_min_f + 1:r_max_f, c_min_f + 1:c_max_f] = True

    # Find all source blocks within the inner mask
    source_instances = find_contiguous_blocks(input_np, source_colors, search_mask=inner_mask)

    # --- Step 6: Apply Templates ---
    # Create mask of cells already painted (initially just the frame)
    painted_mask = (output_np == frame_color)

    for instance in source_instances:
        source_color = instance['color']
        r_abs = instance['r_min'] # Top-left corner of the source instance
        c_abs = instance['c_min']
        
        if source_color in templates:
            template_shape = templates[source_color]
            target_color = mappings[source_color]
            t_h, t_w = template_shape.shape

            # Calculate placement coords relative to output grid's top-left
            r_rel = r_abs - r_min_f
            c_rel = c_abs - c_min_f

            # Apply the template
            for r_t in range(t_h):
                for c_t in range(t_w):
                    out_r = r_rel + r_t
                    out_c = c_rel + c_t

                    # Check bounds of output grid
                    if 0 <= out_r < output_h and 0 <= out_c < output_w:
                        # Check if this cell was already painted
                        if painted_mask[out_r, out_c]:
                            continue

                        template_pixel_color = template_shape[r_t, c_t]
                        
                        # Determine the color to paint based on the template content
                        # The template contains the TARGET color and the BACKGROUND color.
                        if template_pixel_color == target_color:
                             output_color = target_color
                        elif template_pixel_color == background_color:
                             output_color = background_color
                        else:
                             # Template contains unexpected color, skip painting this pixel
                             # This might happen if the component analysis wasn't perfect.
                             continue 
                        
                        output_np[out_r, out_c] = output_color
                        painted_mask[out_r, out_c] = True # Mark as painted
        # else: No template defined for this source color, instance is ignored.

    # Convert final numpy array back to list of lists
    output_grid = output_np.tolist()
    return output_grid
```