import numpy as np
from collections import Counter
import json

# Helper function to convert numpy types to standard Python types for JSON
def convert_numpy_types(obj):
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, np.floating): return float(obj)
    if isinstance(obj, np.ndarray): return obj.tolist()
    if isinstance(obj, set): return sorted([convert_numpy_types(item) for item in obj])
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            key = int(k) if isinstance(k, np.integer) else k
            new_dict[key] = convert_numpy_types(v)
        return new_dict
    if isinstance(obj, list): return [convert_numpy_types(i) for i in obj]
    if isinstance(obj, np.bool_): return bool(obj)
    return obj

def get_neighbors(h, w, r, c):
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < h - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < w - 1: neighbors.append((r, c + 1))
    return neighbors

def find_background_color(grid_np):
    if grid_np.size == 0: return -1
    colors, counts = np.unique(grid_np, return_counts=True)
    if len(colors) == 0: return -1
    return colors[np.argmax(counts)]

def get_source_pixels_and_adjacency(grid_np, background_color):
    h, w = grid_np.shape
    sources = set()
    source_pixel_coords = {}
    source_adjacencies = {color: set() for color in np.unique(grid_np) if color != background_color}

    # First pass: identify all source colors and their locations
    all_non_bg_colors = set(np.unique(grid_np)) - {background_color}
    for color in all_non_bg_colors:
         source_pixel_coords[color] = []

    for r in range(h):
        for c in range(w):
            color = grid_np[r, c]
            if color != background_color:
                source_pixel_coords[color].append((r,c))
                # Check adjacency to background
                is_adj_to_bg = False
                for nr, nc in get_neighbors(h, w, r, c):
                    if grid_np[nr, nc] == background_color:
                        is_adj_to_bg = True
                        break
                if is_adj_to_bg:
                    sources.add(color)

    # Second pass: determine adjacencies between source colors
    for s_color in sources:
        if s_color not in source_pixel_coords: continue
        for r, c in source_pixel_coords[s_color]:
            for nr, nc in get_neighbors(h, w, r, c):
                neighbor_color = grid_np[nr, nc]
                # Check if neighbor is a *different* source color
                if neighbor_color != background_color and neighbor_color != s_color and neighbor_color in sources:
                    source_adjacencies[s_color].add(neighbor_color)

    return sources, source_pixel_coords, source_adjacencies


def derive_map_hypothesis20(sources, source_adjacencies):
    """ Maps S -> S' if S is adjacent to S' and S' > S. Default S -> S. """
    mapping = {}
    for s in sources:
        map_target = s # Default: map to self
        highest_adjacent_source = -1
        # Check adjacent sources
        if s in source_adjacencies:
            for adj_s in source_adjacencies[s]:
                if adj_s > s: # Found adjacent source with higher index
                    if adj_s > highest_adjacent_source:
                        highest_adjacent_source = adj_s

        # If a higher adjacent source was found, map to the highest one
        if highest_adjacent_source != -1:
             map_target = highest_adjacent_source

        mapping[s] = map_target
    return mapping


# --- Input Data ---
# [Same train_inputs and train_outputs]
train_inputs = [
    [[0,0,0,2,2,0,0,0,0,0],[0,0,0,2,0,0,0,0,0,0],[0,0,0,0,1,1,0,0,0,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,0,0,2,0,0],[0,0,0,0,0,0,2,2,0,0],[1,0,0,0,0,0,0,0,0,0],[2,3,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,4,4],[0,0,0,0,0,0,0,0,0,4],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0],[0,1,3,0,4,0,1,1,0,0],[0,4,5,0,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]],
    [[3,3,5,5,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,5,3,3,3,3,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,5,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,2,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,3,4,4,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,4,3,3,1,1,3,3,2,3,3,3],[3,3,3,3,3,3,3,3,3,3,1,3,2,2,3,3,3],[3,3,3,3,3,3,3,3,3,4,3,3,3,3,3,3,3],[3,3,1,6,3,3,3,3,4,4,3,3,3,3,3,3,3],[3,3,2,9,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,4,0,3,3,3,1,3,3,3,3,3,3,3,3,3],[3,3,8,9,3,3,3,1,1,3,3,3,3,3,3,3,3]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,4],[0,0,0,0,0,0,6,6,0,0,0,0,0,0,0,0,4,4],[0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,3,0,0,0,0,0,0,0,0,6,0,0,0,7,7,0,0],[6,7,0,0,0,0,0,0,0,6,6,0,0,0,7,7,0,0],[4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
]
train_outputs = [ # Not used for map derivation, only for comparison
    [[0,0,0,2,2,3,3,3,0,0],[0,0,0,2,3,3,3,3,0,0],[0,0,0,3,1,1,0,3,0,0],[0,0,0,3,1,0,0,3,0,0],[0,0,0,3,0,0,1,3,0,0],[0,0,0,3,0,1,1,3,0,0],[0,0,0,3,3,3,3,2,0,0],[0,0,0,3,3,3,2,2,0,0],[1,0,0,0,0,0,0,0,0,0],[2,3,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,5,5,5,5,4,4],[0,0,0,0,5,5,5,5,5,4],[0,0,0,0,5,1,1,3,5,5],[0,0,0,0,5,1,3,3,5,5],[0,0,0,0,5,3,3,3,5,5],[0,0,0,0,5,3,3,3,5,5],[0,0,0,0,5,3,3,1,5,5],[0,1,3,0,4,3,1,1,5,5],[0,4,5,0,4,4,5,5,5,5],[0,0,0,0,0,0,0,0,0,0]],
    [[3,3,5,5,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,5,3,3,3,3,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,5,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,2,9,9,9,9,9,9,9,9,3,3,3],[3,3,3,3,2,9,9,9,9,9,9,9,9,9,3,3,3],[3,3,3,3,9,9,9,6,6,1,1,9,9,2,3,3,3],[3,3,3,3,9,9,9,6,6,6,1,9,2,2,3,3,3],[3,3,3,3,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,1,6,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,2,9,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,4,0,3,3,3,1,6,6,6,3,3,3,3,3,3],[3,3,8,9,3,3,3,1,1,6,6,3,3,3,3,3,3]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4],[0,0,0,0,0,0,6,6,7,7,7,0,4,4,4,4,4,4],[0,0,0,0,0,0,6,7,7,7,7,0,0,0,0,0,0,0],[0,0,0,0,0,0,7,7,7,7,7,0,0,0,0,0,0,0],[3,3,0,0,0,0,7,7,7,7,6,0,0,0,6,6,0,0],[6,7,0,0,0,0,7,7,7,6,6,0,0,0,6,6,0,0],[4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
]

results = []
# Store maps derived by inference (H15) and hypothesis (H20) for comparison
inferred_maps_h15 = [ # From previous analysis
    {1: 3, 2: 3, 3: 3},
    {1: 3, 4: 5},
    {1: 6, 2: 9, 4: 6},
    {3: 3, 4: 4, 6: 7, 7: 7}
]

for i, (input_grid, output_grid) in enumerate(zip(train_inputs, train_outputs)): # Output only used for observed F
    input_np = np.array(input_grid)
    output_np = np.array(output_grid)

    bg_color = find_background_color(input_np)
    sources, source_coords, source_adj = get_source_pixels_and_adjacency(input_np, bg_color)

    # Derive map using Hypothesis 20
    h20_map = derive_map_hypothesis20(sources, source_adj)
    h20_fill_colors = set(h20_map.values())

    # Get the previously inferred map (H15) for this example
    h15_map = inferred_maps_h15[i]
    h15_fill_colors = set(h15_map.values())

    # Calculate observed fill colors directly for comparison
    mask = (input_np == bg_color)
    fill_colors_observed = set(output_np[mask]) - {bg_color} if np.any(mask) else set()

    results.append({
        "Example": i + 1,
        "Background (BG)": bg_color,
        "Sources (S)": sorted(list(sources)),
        # "Source Adjacencies": source_adj, # Too verbose for summary
        "Hypothesis 20 Map (H20)": h20_map,
        "H20 Fill Colors (F)": sorted(list(h20_fill_colors)),
        "Inferred Map (H15)": h15_map,
        "H15 Fill Colors (F)": sorted(list(h15_fill_colors)),
        "Observed Fill Colors": sorted(list(fill_colors_observed)),
        "H20 Map Correctly Predicts Observed Fills": h20_fill_colors == fill_colors_observed
    })

# Pretty print results using the converter
print(json.dumps(convert_numpy_types(results), indent=2))
