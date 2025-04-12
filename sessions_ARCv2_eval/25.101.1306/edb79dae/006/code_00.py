import numpy as np
from collections import Counter, deque
from typing import List, Dict, Tuple, Set, Optional

# --- Data ---
input_grid_1 = [[1, 1, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 1, 4, 8, 8, 1, 8, 1, 8, 8, 3, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 4, 4, 8, 8, 1, 1, 1, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 3, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8]]
input_grid_2 = [[2, 2, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 4, 1, 1, 2, 2, 2, 2, 1, 3, 3, 3, 3, 1, 1, 6, 6, 6, 6, 1, 1], [2, 2, 4, 4, 1, 1, 2, 2, 2, 2, 1, 1, 3, 3, 1, 1, 1, 6, 6, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 3, 3, 3, 3, 1, 1, 6, 6, 1, 1, 1, 1], [3, 3, 8, 8, 1, 1, 2, 1, 2, 2, 1, 3, 1, 1, 3, 1, 1, 6, 6, 6, 6, 1, 1], [3, 3, 3, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [3, 3, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 6, 7, 7, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [6, 6, 6, 7, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [6, 6, 7, 7, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

frame_color = 5

# --- Helper Functions (Using previous definitions - assume they work for BBox and finding components) ---

def find_frame_bbox(grid_np: np.ndarray, frame_color: int = 5) -> Optional[Tuple[int, int, int, int]]:
    coords = np.argwhere(grid_np == frame_color)
    if coords.size == 0: return None
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)
    if r_max < r_min + 2 or c_max < c_min + 2: return None
    on_border_check = (coords[:, 0] == r_min) | (coords[:, 0] == r_max) | \
                      (coords[:, 1] == c_min) | (coords[:, 1] == c_max)
    if not np.all(on_border_check): return None
    inner_slice = grid_np[r_min + 1:r_max, c_min + 1:c_max]
    if np.any(inner_slice == frame_color): return None
    return (r_min, c_min, r_max, c_max)

def analyze_key_area_refined(grid_np: np.ndarray, frame_bbox: Tuple[int, int, int, int], frame_color: int) -> Optional[Tuple[Dict[int, int], int, Dict[int, np.ndarray]]]:
    rows, cols = grid_np.shape
    r_min_f, c_min_f, r_max_f, c_max_f = frame_bbox
    
    key_area_mask = np.ones_like(grid_np, dtype=bool)
    key_area_mask[r_min_f:r_max_f + 1, c_min_f:c_max_f + 1] = False
    key_area_coords = np.argwhere(key_area_mask)

    if key_area_coords.size == 0: return None # No key area

    outside_colors_counter = Counter()
    for r, c in key_area_coords:
        outside_colors_counter[grid_np[r, c]] += 1
    
    if not outside_colors_counter: return None

    # --- Find Background Color ---
    # Assume background is most frequent color NOT involved in potential pairs later
    # Keep list sorted by freq (desc), color (asc)
    sorted_outside_colors = sorted(outside_colors_counter.items(), key=lambda item: (-item[1], item[0]))
    
    # --- Find Solid & Pattern Blocks ---
    visited_key = np.zeros_like(grid_np, dtype=bool)
    visited_key[~key_area_mask] = True 

    solid_blocks = []         # Blocks of a single color S
    pattern_blocks = []       # Blocks containing color T + potential background B

    potential_background = sorted_outside_colors[0][0] # Initial guess

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
                colors_in_component.add(color)
                component_coords.add((r,c))
                r_min_comp, c_min_comp = min(r_min_comp, r), min(c_min_comp, c)
                r_max_comp, c_max_comp = max(r_max_comp, r), max(c_max_comp, c)

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not visited_key[nr, nc]:
                        visited_key[nr, nc] = True
                        q.append((nr, nc))

            # --- Categorize ---
            # A component is SOLID if it contains exactly one color.
            if len(colors_in_component) == 1:
                color_s = list(colors_in_component)[0]
                # Check if it's the potential background - background cannot be a solid source block
                if color_s != potential_background:
                    solid_blocks.append({
                        'color': color_s, 'coords': component_coords,
                        'r_min': r_min_comp, 'c_min': c_min_comp
                    })
            # A component is a PATTERN CANDIDATE if it contains exactly two colors,
            # one of which is the potential background.
            elif len(colors_in_component) == 2 and potential_background in colors_in_component:
                color_t = list(colors_in_component - {potential_background})[0]
                pattern_arr = grid_np[r_min_comp:r_max_comp+1, c_min_comp:c_max_comp+1].copy()
                pattern_blocks.append({
                     'target_color': color_t, 
                     'potential_bg': potential_background,
                     'coords': component_coords,
                     'r_min': r_min_comp, 'c_min': c_min_comp,
                     'array': pattern_arr
                 })

    # --- Finalize Background & Find Mappings by Adjacency ---
    solid_colors = {b['color'] for b in solid_blocks}
    target_colors = {p['target_color'] for p in pattern_blocks}
    
    background_color = -1
    for color, count in sorted_outside_colors:
        if color not in solid_colors and color not in target_colors:
            background_color = color
            break
            
    if background_color == -1: # Fallback if all colors involved somehow
        background_color = potential_background 
        print(f"Warning: Could not definitively separate background. Using initial guess: {background_color}")

    # Filter pattern blocks based on final background
    valid_patterns = [p for p in pattern_blocks if p['potential_bg'] == background_color]
    
    mappings = {}
    templates = {}
    
    for sb in solid_blocks:
        source_color = sb['color']
        if source_color in mappings: continue
        
        adjacent_pattern = None
        for pb in valid_patterns:
            # Check adjacency efficiently
            is_adjacent = False
            for r_s, c_s in sb['coords']:
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                     nr, nc = r_s + dr, c_s + dc
                     if (nr, nc) in pb['coords']:
                         is_adjacent = True
                         break
                 if is_adjacent: break
            if is_adjacent:
                 # Ensure this pattern's target color isn't already mapped FROM another source
                 target_color = pb['target_color']
                 # Check if target color is already a value in mappings
                 already_mapped_to = False
                 for mapped_target in mappings.values():
                     if mapped_target == target_color:
                         already_mapped_to = True
                         break
                 if not already_mapped_to:
                     adjacent_pattern = pb
                     break # Found adjacent pattern for this solid block

        if adjacent_pattern:
            target_color = adjacent_pattern['target_color']
            mappings[source_color] = target_color
            templates[source_color] = adjacent_pattern['array']
            
    if not mappings: return None

    return mappings, background_color, templates


# --- Analysis ---
results = {}
for i, grid in enumerate([input_grid_1, input_grid_2]):
    name = f"train_{i+1}"
    print(f"--- Analyzing {name} ---")
    input_np = np.array(grid)
    frame_bbox = find_frame_bbox(input_np, frame_color)
    if frame_bbox:
        print(f"Frame: {frame_bbox}")
        analysis_result = analyze_key_area_refined(input_np, frame_bbox, frame_color)
        if analysis_result:
            mappings, background, templates_shapes = analysis_result
            results[name] = {
                "background": background,
                "mappings": mappings,
                "templates": {k: v.shape for k,v in templates_shapes.items()}
            }
            print(f"Background: {background}")
            print(f"Mappings (Source -> Target): {mappings}")
            print(f"Templates Assigned (Source -> Shape): {results[name]['templates']}")
            if len(mappings) != len(templates_shapes):
                 print("Warning: Mismatch between mappings found and templates assigned!")
        else:
            print(f"Error: Could not analyze key area for {name}")
            results[name] = {"error": "Key area analysis failed"}
    else:
        print("No frame found.")
        results[name] = {"error": "No frame found"}
