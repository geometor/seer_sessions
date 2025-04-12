import numpy as np
from collections import Counter, deque

# --- Data ---
# train_1 input
input_grid_1 = [[1, 1, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 1, 4, 8, 8, 1, 8, 1, 8, 8, 3, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 4, 4, 8, 8, 1, 1, 1, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 3, 3, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 3, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [3, 3, 2, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 3, 3, 3, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 3, 3, 3, 8, 1, 1, 1, 8, 8, 8, 8, 8, 3, 3, 3, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 3, 3, 3, 8, 1, 1, 1, 8, 1, 1, 1, 8, 5, 8, 8], [8, 8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 8, 8], [8, 8, 8, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 8, 8]]
# train_2 input
input_grid_2 = [[2, 2, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 4, 1, 1, 2, 2, 2, 2, 1, 3, 3, 3, 3, 1, 1, 6, 6, 6, 6, 1, 1], [2, 2, 4, 4, 1, 1, 2, 2, 2, 2, 1, 1, 3, 3, 1, 1, 1, 6, 6, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 3, 3, 3, 3, 1, 1, 6, 6, 1, 1, 1, 1], [3, 3, 8, 8, 1, 1, 2, 1, 2, 2, 1, 3, 1, 1, 3, 1, 1, 6, 6, 6, 6, 1, 1], [3, 3, 3, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [3, 3, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 6, 7, 7, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [6, 6, 6, 7, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [6, 6, 7, 7, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 3, 3, 3, 3, 1, 5], [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6, 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 3, 3, 3, 3, 1, 2, 2, 2, 2, 1, 6, 6 6, 6, 1, 5], [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

frame_color = 5

# --- Helper Functions (Adapted) ---

def find_frame_bbox(grid_np: np.ndarray, frame_color: int = 5) -> tuple[int, int, int, int] | None:
    # (Same as previous version - assumed correct for now)
    coords = np.argwhere(grid_np == frame_color)
    if coords.size == 0: return None
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)
    on_border = (coords[:, 0] == r_min) | (coords[:, 0] == r_max) | \
                (coords[:, 1] == c_min) | (coords[:, 1] == c_max)
    if not np.all(on_border): return None
    if r_max > r_min + 1 and c_max > c_min + 1:
        inner_slice = grid_np[r_min + 1:r_max, c_min + 1:c_max]
        if np.any(inner_slice == frame_color): return None
    return (r_min, c_min, r_max, c_max)

def find_blocks_outside_frame(grid_np: np.ndarray, frame_bbox: tuple[int, int, int, int], frame_color: int):
    """Finds solid blocks and template blocks outside the frame."""
    rows, cols = grid_np.shape
    r_min, c_min, r_max, c_max = frame_bbox
    visited = np.zeros_like(grid_np, dtype=bool)
    
    # Mark frame area as visited to ignore it
    visited[r_min:r_max+1, c_min:c_max+1] = True
    
    solid_blocks = [] # {color, coords, r_min, c_min, r_max, c_max}
    template_blocks = [] # {target_color, background_color, coords, r_min, c_min, r_max, c_max, array}
    
    # First pass: Identify potential background color
    outside_colors_counter = Counter()
    for r in range(rows):
        for c in range(cols):
            if not visited[r,c]: # Outside frame
                 color = grid_np[r,c]
                 if color != frame_color: # Should always be true here
                     outside_colors_counter[color]+=1
    
    potential_background = -1
    if outside_colors_counter:
        # Simple most frequent for now, refinement needed later
        potential_background = outside_colors_counter.most_common(1)[0][0] 
    else:
        potential_background = 0 # Default

    # Second pass: BFS to find components outside frame
    for r_init in range(rows):
        for c_init in range(cols):
            if not visited[r_init, c_init]:
                component_coords = set()
                colors_in_component = set()
                q = deque([(r_init, c_init)])
                visited[r_init, c_init] = True
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
                        # Check bounds and if outside frame (implicitly true if not visited)
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]: 
                             # Check if connected pixel has same color OR is potential background
                             # This definition might need adjustment based on examples
                             neighbor_color = grid_np[nr, nc]
                             # *** Crucial Decision: How are components defined? ***
                             # Option 1: Only same color (finds solid blocks easily)
                             # Option 2: Same color OR background (tries to find templates)
                             # Option 3: Any non-frame color (finds all connected stuff)
                             
                             # Let's try Option 3 first to categorize components, then analyze
                             visited[nr, nc] = True
                             q.append((nr, nc))
                             
                # --- Categorize the found component ---
                non_background_colors = colors_in_component - {potential_background}
                
                if len(non_background_colors) == 1:
                    single_color = list(non_background_colors)[0]
                    # Is it a solid block or a template block?
                    if len(colors_in_component) == 1: # Only the single color present
                         solid_blocks.append({
                             'color': single_color, 'coords': component_coords,
                             'r_min': r_min_comp, 'c_min': c_min_comp,
                             'r_max': r_max_comp, 'c_max': c_max_comp
                         })
                    elif len(colors_in_component) == 2 and potential_background in colors_in_component:
                         # Contains the single color and the background -> Template
                         template_arr = grid_np[r_min_comp:r_max_comp+1, c_min_comp:c_max_comp+1]
                         template_blocks.append({
                             'target_color': single_color, 
                             'background_color': potential_background, 
                             'coords': component_coords,
                             'r_min': r_min_comp, 'c_min': c_min_comp,
                             'r_max': r_max_comp, 'c_max': c_max_comp,
                             'array': template_arr
                         })
                    # else: More than 2 colors or just background -> ignore for mapping
                # else: More than 1 non-background color or only background -> ignore

    # --- Refine Background and Find Mappings ---
    mapped_colors = set()
    mappings = {} # source_color -> target_color
    templates = {} # source_color -> template_array

    # Collect colors involved in solid and template blocks
    solid_colors = {b['color'] for b in solid_blocks}
    target_colors = {b['target_color'] for b in template_blocks}
    
    # Find actual background: most frequent OUTSIDE color NOT in solid_colors or target_colors
    actual_background = -1
    sorted_outside = sorted(outside_colors_counter.items(), key=lambda item: (-item[1], item[0]))
    possible_mapping_colors = solid_colors | target_colors
    for color, count in sorted_outside:
        if color not in possible_mapping_colors:
             actual_background = color
             break
    if actual_background == -1: # Fallback if conflict
        actual_background = potential_background 
        
    # Re-filter template blocks if potential_background was wrong
    valid_template_blocks = [
        tb for tb in template_blocks if tb['background_color'] == actual_background
    ]
    
    # Find adjacency between SOLID (Source) and TEMPLATE (Target+BG) blocks
    for sb in solid_blocks:
        source_color = sb['color']
        if source_color in mappings: continue # Already mapped

        for tb in valid_template_blocks:
            target_color = tb['target_color']
            if target_color in mappings.values(): continue # Already mapped to

            # Check adjacency (simple check: bounding box proximity + 1 pixel check)
            # A more robust check looks at actual coordinate adjacency
            is_adjacent = False
            for r_s, c_s in sb['coords']:
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                     nr, nc = r_s + dr, c_s + dc
                     if (nr, nc) in tb['coords']:
                         is_adjacent = True
                         break
                 if is_adjacent: break
                 
            if is_adjacent:
                 mappings[source_color] = target_color
                 templates[source_color] = tb['array']
                 mapped_colors.add(source_color)
                 mapped_colors.add(target_color)
                 break # Found mapping for this source color

    # Final check on background - ensure it wasn't accidentally part of a mapped pair
    if actual_background in mapped_colors:
        # This indicates an issue, try second most frequent non-mapped?
        print(f"Warning: Background color {actual_background} seems to be involved in mapping.")
        # Attempt to find a new background
        new_background = -1
        possible_mapping_colors = set(mappings.keys()) | set(mappings.values())
        for color, count in sorted_outside:
             if color not in possible_mapping_colors:
                 new_background = color
                 break
        if new_background != -1:
            print(f"Switching background to {new_background}")
            actual_background = new_background
        else:
            print("Could not find alternative background. Proceeding with caution.")


    return actual_background, solid_blocks, valid_template_blocks, mappings, templates


# --- Analysis ---
results = {}
for i, grid in enumerate([input_grid_1, input_grid_2]):
    name = f"train_{i+1}"
    print(f"--- Analyzing {name} ---")
    input_np = np.array(grid)
    frame_bbox = find_frame_bbox(input_np, frame_color)
    if frame_bbox:
        print(f"Frame: {frame_bbox}")
        try:
            background, solid, templates_found, mappings, templates_shapes = find_blocks_outside_frame(input_np, frame_bbox, frame_color)
            results[name] = {
                "background": background,
                "mappings": mappings,
                "templates": templates_shapes # {source: array}
            }
            print(f"Background: {background}")
            print(f"Mappings (Source -> Target): {mappings}")
            # print(f"Solid Blocks Found: {len(solid)}")
            # print(f"Template Blocks Found (Target+BG): {len(templates_found)}")
            print(f"Templates Assigned (Source -> Shape): { {k: v.shape for k,v in templates_shapes.items()} }")
            if len(mappings) != len(templates_shapes):
                 print("Warning: Mismatch between mappings found and templates assigned!")

        except Exception as e:
            print(f"Error analyzing {name}: {e}")
            results[name] = {"error": str(e)}
    else:
        print("No frame found.")
        results[name] = {"error": "No frame found"}

# print("\n--- Summary ---")
# print(results)
