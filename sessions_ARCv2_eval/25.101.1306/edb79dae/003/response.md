```python
import numpy as np
from collections import Counter, deque

"""
Transforms the input grid by:
1. Identifying a rectangular gray (5) frame.
2. Analyzing the area outside the frame to find:
    a. Color mapping rules (A -> B) based on adjacent blocks.
    b. The invariant background color (most frequent outside color not involved in mappings or the frame).
    c. Template blocks for each source color 'A', composed of color 'A' and the background color.
3. Creating an output grid based on the frame size, initialized with the background color.
4. Copying the gray frame to the output.
5. Finding contiguous blocks of source colors 'A' inside the frame.
6. For each source block found, retrieving its corresponding template, substituting color 'A' with 'B', 
   and drawing this transformed template onto the output grid at the source block's location.
"""

def find_frame_bbox(grid_np: np.ndarray, frame_color: int = 5) -> tuple[int, int, int, int] | None:
    """
    Finds the bounding box coordinates (min_row, min_col, max_row, max_col) 
    of the largest rectangular frame made of frame_color.
    Checks if the identified structure forms a hollow rectangle.
    Returns None if no such frame is found.
    """
    coords = np.argwhere(grid_np == frame_color)
    if coords.size == 0:
        return None
        
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)

    # Verify it's a hollow rectangle
    # All frame_color pixels must be on the border
    on_border = (coords[:, 0] == r_min) | (coords[:, 0] == r_max) | \
                (coords[:, 1] == c_min) | (coords[:, 1] == c_max)
    if not np.all(on_border):
        # Could potentially search for smaller frames, but assume largest for now
        return None 

    # Check if the inside is not the frame color (ensure it's hollow)
    # Avoid checking if frame is only 1 or 2 pixels wide/high
    if r_max > r_min + 1 and c_max > c_min + 1:
        inner_slice = grid_np[r_min + 1:r_max, c_min + 1:c_max]
        if np.any(inner_slice == frame_color):
            return None # Frame color found inside, not a simple hollow frame

    return (r_min, c_min, r_max, c_max)

def find_contiguous_blocks(grid_np: np.ndarray, target_colors: set[int], start_coord: tuple[int, int] | None = None) -> list[dict]:
    """
    Finds all contiguous blocks of any single color within target_colors.
    Returns a list of dictionaries, each containing 'color', 'coords' (set), 
    'r_min', 'c_min', 'r_max', 'c_max'.
    If start_coord is provided, only finds the block containing that coordinate.
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    blocks = []
    
    search_coords = []
    if start_coord:
        search_coords = [start_coord]
    else:
        # Generate all coordinates if no start_coord is given
        search_coords = [(r, c) for r in range(rows) for c in range(cols)]

    for r_init, c_init in search_coords:
        color = grid_np[r_init, c_init]
        if color in target_colors and not visited[r_init, c_init]:
            block_coords = set()
            q = deque([(r_init, c_init)])
            visited[r_init, c_init] = True
            r_min, c_min = r_init, c_init
            r_max, c_max = r_init, c_init
            
            while q:
                r, c = q.popleft()
                block_coords.add((r, c))
                r_min, c_min = min(r_min, r), min(c_min, c)
                r_max, c_max = max(r_max, r), max(c_max, c)

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       not visited[nr, nc] and grid_np[nr, nc] == color:
                        visited[nr, nc] = True
                        q.append((nr, nc))

            blocks.append({
                'color': color, 
                'coords': block_coords,
                'r_min': r_min, 'c_min': c_min, 
                'r_max': r_max, 'c_max': c_max
            })
            # If we started with a specific coordinate, we found its block, so break
            if start_coord:
                 break 
                 
    return blocks

def find_template_blocks(grid_np: np.ndarray, source_colors: set[int], background_color: int) -> dict[int, np.ndarray]:
    """
    Finds template blocks outside the frame. A template block for source color 'A' 
    is a contiguous component made ONLY of color 'A' and the background_color, 
    containing at least one pixel of color 'A'.
    Returns a dictionary {source_color: template_array}.
    Assumes the relevant template is the first one found for each source color.
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    templates = {}
    allowed_colors = source_colors | {background_color}

    for r_init in range(rows):
        for c_init in range(cols):
            # Start BFS from a source color pixel that hasn't been visited
            start_color = grid_np[r_init, c_init]
            if start_color in source_colors and not visited[r_init, c_init] and start_color not in templates:
                
                component_coords = set()
                q = deque([(r_init, c_init)])
                visited[r_init, c_init] = True
                r_min, c_min = r_init, c_init
                r_max, c_max = r_init, c_init
                found_source_color = False 
                
                while q:
                    r, c = q.popleft()
                    current_color = grid_np[r, c]
                    
                    # Check if the component contains invalid colors
                    if current_color not in allowed_colors:
                        # Mark all visited in this path as invalid? Difficult.
                        # Easier to validate after BFS finds the full component.
                        # For now, just skip adding this coord and continue BFS elsewhere.
                        # A better approach might be needed if templates intermingle badly.
                         continue 

                    component_coords.add((r, c))
                    if current_color == start_color:
                        found_source_color = True
                    
                    r_min, c_min = min(r_min, r), min(c_min, c)
                    r_max, c_max = max(r_max, r), max(c_max, c)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid_np[nr, nc] in allowed_colors:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Post-BFS validation: Ensure component only has start_color & background
                is_valid_template = True
                if not found_source_color: # Should not happen if start_color is source
                    is_valid_template = False
                else:
                    for r_comp, c_comp in component_coords:
                        if grid_np[r_comp, c_comp] not in [start_color, background_color]:
                            is_valid_template = False
                            break
                
                if is_valid_template:
                    # Extract the bounding box as the template
                    template_arr = grid_np[r_min:r_max + 1, c_min:c_max + 1]
                    templates[start_color] = template_arr
                    # Optimization: If we found templates for all source colors, stop.
                    if len(templates) == len(source_colors):
                        break
            
            # If we found templates for all source colors, stop outer loop.
            if len(templates) == len(source_colors):
                 break
                        
    return templates


def analyze_key_area(grid_np: np.ndarray, frame_bbox: tuple[int, int, int, int], frame_color: int) -> tuple[dict[int, int], int, dict[int, np.ndarray]]:
    """
    Analyzes the area outside the frame to find mappings, background, and templates.
    """
    rows, cols = grid_np.shape
    r_min, c_min, r_max, c_max = frame_bbox

    outside_colors_counter = Counter()
    outside_coords_map = {} # Store coords for each color
    key_area_mask = np.ones_like(grid_np, dtype=bool)
    key_area_mask[r_min:r_max+1, c_min:c_max+1] = False # Mask out frame area

    for r in range(rows):
        for c in range(cols):
            if key_area_mask[r, c]: # If outside frame
                color = grid_np[r, c]
                if color != frame_color:
                    outside_colors_counter[color] += 1
                    if color not in outside_coords_map:
                        outside_coords_map[color] = []
                    outside_coords_map[color].append((r,c))

    # --- Find Mappings using block adjacency ---
    mappings = {}
    mapped_colors = set()
    potential_keys = set(outside_colors_counter.keys())
    
    # Find blocks for all potential key colors outside the frame
    outside_blocks_map = {} # {color: [block_info, ...]}
    for color in potential_keys:
        if color in outside_coords_map:
            # Create a temporary grid containing only this color and -1 elsewhere
            temp_grid = np.full_like(grid_np, -1)
            for r, c in outside_coords_map[color]:
                 temp_grid[r, c] = color
            
            # Find blocks of this color in the temp grid (ensures only outside blocks)
            blocks = find_contiguous_blocks(temp_grid, {color})
            if blocks:
                 outside_blocks_map[color] = blocks

    # Check adjacency between blocks of different colors
    colors_present = list(outside_blocks_map.keys())
    for i in range(len(colors_present)):
        color_a = colors_present[i]
        if color_a in mapped_colors: continue # Already used as key or value

        for j in range(i + 1, len(colors_present)):
            color_b = colors_present[j]
            if color_b in mapped_colors: continue

            # Check if any block of color_a is adjacent to any block of color_b
            found_adjacency = False
            for block_a in outside_blocks_map[color_a]:
                coords_a = block_a['coords']
                for block_b in outside_blocks_map[color_b]:
                    coords_b = block_b['coords']
                    
                    # Check horizontal/vertical adjacency
                    for r_a, c_a in coords_a:
                        is_adjacent = False
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = r_a + dr, c_a + dc
                            if (nr, nc) in coords_b:
                                is_adjacent = True
                                break
                        if is_adjacent:
                            found_adjacency = True
                            break
                if found_adjacency:
                    break
            
            if found_adjacency:
                 # Found an adjacent pair (A, B). Need to decide direction.
                 # Heuristic: Assume the block appearing "first" (min row, then min col) is the key.
                 a_min_r = min(b['r_min'] for b in outside_blocks_map[color_a])
                 a_min_c = min(b['c_min'] for b in outside_blocks_map[color_a] if b['r_min'] == a_min_r)
                 b_min_r = min(b['r_min'] for b in outside_blocks_map[color_b])
                 b_min_c = min(b['c_min'] for b in outside_blocks_map[color_b] if b['r_min'] == b_min_r)

                 key_color, val_color = -1, -1
                 if (a_min_r < b_min_r) or (a_min_r == b_min_r and a_min_c < b_min_c):
                      key_color, val_color = color_a, color_b
                 else:
                      key_color, val_color = color_b, color_a
                      
                 if key_color not in mappings:
                    mappings[key_color] = val_color
                    mapped_colors.add(key_color)
                    mapped_colors.add(val_color)
                    # Break inner loops once a mapping is found for color_a?
                    # Let's assume one mapping pair per distinct visual pair.
                 
                 # Avoid mapping the same colors again
                 break # Move to the next color_a

    # --- Determine Background Color ---
    background_color = -1
    sorted_colors = sorted(outside_colors_counter.items(), key=lambda item: (-item[1], item[0]))
    for color, count in sorted_colors:
        if color not in mapped_colors:
            background_color = color
            break
            
    if background_color == -1: # Fallback if all outside colors are mapped
        # Check inside frame (excluding border) for most frequent non-mapped, non-frame color
        if r_max > r_min and c_max > c_min:
            inside_counter = Counter()
            for r in range(r_min + 1, r_max):
                for c in range(c_min + 1, c_max):
                    color = grid_np[r, c]
                    if color != frame_color and color not in mapped_colors:
                        inside_counter[color] += 1
            sorted_inside = sorted(inside_counter.items(), key=lambda item: (-item[1], item[0]))
            if sorted_inside:
                background_color = sorted_inside[0][0]
            else:
                background_color = 0 # Ultimate fallback
        else:
             background_color = 0 # Frame too small for interior


    # --- Find Templates ---
    source_colors = set(mappings.keys())
    # Create a copy of the grid where the frame area is marked invalid for template search
    key_area_grid = grid_np.copy()
    # Mark frame and inside with a value not in allowed_colors for find_template_blocks
    invalid_marker = -99 
    key_area_grid[r_min:r_max+1, c_min:c_max+1] = invalid_marker
    
    templates = find_template_blocks(key_area_grid, source_colors, background_color)
    
    # Validation: Ensure templates were found for all source colors
    if len(templates) != len(source_colors):
         print(f"Warning: Could not find templates for all source colors. Found: {templates.keys()}, Needed: {source_colors}")
         # Handle this case? Maybe default to simple color swap? For now, proceed.

    return mappings, background_color, templates


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Main transformation function.
    """
    input_np = np.array(input_grid, dtype=int)
    frame_color = 5

    # --- Step 1: Find the Frame ---
    frame_bbox = find_frame_bbox(input_np, frame_color)
    if frame_bbox is None:
        # print("Warning: No valid frame found. Returning input grid unchanged.")
        return input_grid
    r_min, c_min, r_max, c_max = frame_bbox

    # --- Step 2: Analyze Key Area (Outside Frame) ---
    try:
        mappings, background_color, templates = analyze_key_area(input_np, frame_bbox, frame_color)
    except Exception as e:
        # print(f"Error during key area analysis: {e}. Returning input grid.")
        # Fallback or error handling - return original grid might be safest
        return input_grid # Or raise error

    # --- Step 3: Initialize Output ---
    output_h = r_max - r_min + 1
    output_w = c_max - c_min + 1
    output_np = np.full((output_h, output_w), background_color, dtype=int)

    # --- Step 4: Copy Frame ---
    # Iterate through the frame coordinates found initially
    frame_coords_relative = np.argwhere(input_np[r_min:r_max+1, c_min:c_max+1] == frame_color)
    for r_rel, c_rel in frame_coords_relative:
        output_np[r_rel, c_rel] = frame_color

    # --- Step 5: Identify and Transform Source Blocks ---
    source_colors = set(mappings.keys())
    # Create a grid representing only the inside of the frame
    inside_grid_np = input_np[r_min + 1:r_max, c_min + 1:c_max]
    
    # Need to keep track of visited cells in the *output* grid's coordinate system
    # to avoid overwriting parts of placed templates by later blocks.
    output_visited_mask = np.zeros_like(output_np, dtype=bool) 
    # Mark frame as visited initially
    output_visited_mask[output_np == frame_color] = True 

    # Iterate through potential starting points inside the frame
    for r_in in range(inside_grid_np.shape[0]):
        for c_in in range(inside_grid_np.shape[1]):
            # Map inside coords (r_in, c_in) to output coords (r_out, c_out)
            r_out, c_out = r_in + 1, c_in + 1 
            
            # Check if this output cell has already been processed (part of another template or frame)
            if output_visited_mask[r_out, c_out]:
                continue

            source_color = inside_grid_np[r_in, c_in]

            if source_color in source_colors:
                 # We found a potential start of a source block. 
                 # Find the full block in the *original* input grid, starting from global coords.
                 global_r, global_c = r_in + r_min + 1, c_in + c_min + 1
                 
                 # Find the single block containing this global coordinate
                 source_block_info_list = find_contiguous_blocks(input_np, {source_color}, start_coord=(global_r, global_c))
                 
                 if source_block_info_list: # Should find exactly one block
                     source_block_info = source_block_info_list[0]
                     block_r_min_global = source_block_info['r_min']
                     block_c_min_global = source_block_info['c_min']
                     
                     # Calculate top-left relative to the output grid
                     block_r_rel = block_r_min_global - r_min
                     block_c_rel = block_c_min_global - c_min

                     # Check if we have a template for this color
                     if source_color in templates:
                         template = templates[source_color]
                         target_color = mappings[source_color]
                         t_h, t_w = template.shape

                         # Apply the template
                         for r_t in range(t_h):
                             for c_t in range(t_w):
                                 out_r = block_r_rel + r_t
                                 out_c = block_c_rel + c_t

                                 # Ensure placement is within output bounds
                                 if 0 <= out_r < output_h and 0 <= out_c < output_w:
                                     template_pixel = template[r_t, c_t]
                                     # Only overwrite if not already visited (e.g., by frame or another template)
                                     if not output_visited_mask[out_r, out_c]:
                                         if template_pixel == source_color:
                                             output_np[out_r, out_c] = target_color
                                         elif template_pixel == background_color:
                                             # Already initialized with background, but mark visited
                                             output_np[out_r, out_c] = background_color 
                                         # else: # Should not happen if template is valid
                                         #     print(f"Warning: Unexpected color {template_pixel} in template for {source_color}")
                                         
                                         # Mark this output cell as visited
                                         output_visited_mask[out_r, out_c] = True
                     else:
                         # No template found - what to do? Simple color swap? Skip?
                         # For now, let's mark the block's area as visited to avoid reprocessing
                         # coords_global = source_block_info['coords']
                         # for r_g, c_g in coords_global:
                         #      r_o, c_o = r_g - r_min, c_g - c_min
                         #      if 0 <= r_o < output_h and 0 <= c_o < output_w:
                         #           output_visited_mask[r_o, c_o] = True
                         # print(f"Warning: No template for source color {source_color} at ({block_r_rel}, {block_c_rel}). Skipping block.")
                         pass # Mark as visited below

                     # Mark the entire original source block area in the output as visited,
                     # regardless of template application, to prevent reprocessing pixels
                     # of the same block if the BFS in find_contiguous_blocks was used earlier.
                     # Find the coordinates relative to the output grid.
                     coords_global = source_block_info['coords']
                     for r_g, c_g in coords_global:
                         r_o, c_o = r_g - r_min, c_g - c_min
                         if 0 <= r_o < output_h and 0 <= c_o < output_w:
                              output_visited_mask[r_o, c_o] = True
                 # else: # Should not happen if find_contiguous_blocks works
                 #     print(f"Error: Did not find block for source color {source_color} starting at global ({global_r}, {global_c})")
                 #     output_visited_mask[r_out, c_out] = True # Mark start cell visited anyway

            else:
                # If the cell inside is not a source color, just mark it visited if it's background
                # (Other colors inside that aren't source colors are ignored per the logic)
                if source_color == background_color:
                     output_visited_mask[r_out, c_out] = True


    # --- Step 6: Output ---
    output_grid = output_np.tolist()
    return output_grid
```