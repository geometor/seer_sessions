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

def get_source_pixels(grid_np, background_color):
    h, w = grid_np.shape
    sources = set()
    source_pixel_coords = {color: [] for color in np.unique(grid_np) if color != background_color}
    processed_sources = set()

    for r in range(h):
        for c in range(w):
            color = grid_np[r, c]
            if color != background_color:
                source_pixel_coords[color].append((r,c))
                # Check adjacency only once per source color type for efficiency
                if color not in processed_sources:
                    is_adj_to_bg = False
                    for nr, nc in get_neighbors(h, w, r, c):
                        if grid_np[nr, nc] == background_color:
                            is_adj_to_bg = True
                            break
                    if is_adj_to_bg:
                        sources.add(color)
                        processed_sources.add(color) # Mark as checked

    # Verify all non-BG colors were considered (should be redundant if loops correct)
    all_non_bg = set(np.unique(grid_np)) - {background_color}
    if sources != all_non_bg:
         # This indicates some non-BG colors are *not* adjacent to BG (PFDs exist)
         # For *this* specific task based on previous analysis, S seems to equal all non-BG
         pass # Keep sources as only those adjacent

    return sources, source_pixel_coords

def infer_mapping(input_np, output_np, bg_color, sources, source_coords):
    h, w = input_np.shape
    mapping = {}
    for s_color in sources:
        adjacent_bg_pixels_output_colors = []
        # Find all input BG pixels adjacent to *any* pixel of s_color
        if s_color not in source_coords: continue # Skip if source has no pixels

        for r_s, c_s in source_coords[s_color]:
            for nr, nc in get_neighbors(h, w, r_s, c_s):
                # Check if neighbor was background in input
                if input_np[nr, nc] == bg_color:
                    # Get the color of this pixel in the output
                    output_color = output_np[nr, nc]
                    # Only consider changed pixels (output != bg)
                    if output_color != bg_color:
                        adjacent_bg_pixels_output_colors.append(output_color)

        # Find the most frequent non-background output color among these pixels
        if adjacent_bg_pixels_output_colors:
            counts = Counter(adjacent_bg_pixels_output_colors)
            # Find the color with the maximum count
            # If there are ties, Counter.most_common(1) returns one arbitrarily (usually first encountered)
            # ARC often requires deterministic tie-breaking, e.g., lowest color index.
            # Let's implement tie-breaking:
            max_count = 0
            most_common_colors = []
            for color, count in counts.items():
                 if count > max_count:
                     max_count = count
                     most_common_colors = [color]
                 elif count == max_count:
                     most_common_colors.append(color)

            if most_common_colors:
                 # Tie-break by choosing the color with the lowest index
                 mapped_color = min(most_common_colors)
                 mapping[s_color] = mapped_color

    return mapping

# --- Input Data ---
# [Same train_inputs and train_outputs as previous attempt]
train_inputs = [
    [[0,0,0,2,2,0,0,0,0,0],[0,0,0,2,0,0,0,0,0,0],[0,0,0,0,1,1,0,0,0,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,0,0,2,0,0],[0,0,0,0,0,0,2,2,0,0],[1,0,0,0,0,0,0,0,0,0],[2,3,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,4,4],[0,0,0,0,0,0,0,0,0,4],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0],[0,1,3,0,4,0,1,1,0,0],[0,4,5,0,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]],
    [[3,3,5,5,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,5,3,3,3,3,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,5,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,2,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,3,4,4,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,4,3,3,1,1,3,3,2,3,3,3],[3,3,3,3,3,3,3,3,3,3,1,3,2,2,3,3,3],[3,3,3,3,3,3,3,3,3,4,3,3,3,3,3,3,3],[3,3,1,6,3,3,3,3,4,4,3,3,3,3,3,3,3],[3,3,2,9,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,4,0,3,3,3,1,3,3,3,3,3,3,3,3,3],[3,3,8,9,3,3,3,1,1,3,3,3,3,3,3,3,3]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,4],[0,0,0,0,0,0,6,6,0,0,0,0,0,0,0,0,4,4],[0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,3,0,0,0,0,0,0,0,0,6,0,0,0,7,7,0,0],[6,7,0,0,0,0,0,0,0,6,6,0,0,0,7,7,0,0],[4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
]
train_outputs = [
    [[0,0,0,2,2,3,3,3,0,0],[0,0,0,2,3,3,3,3,0,0],[0,0,0,3,1,1,0,3,0,0],[0,0,0,3,1,0,0,3,0,0],[0,0,0,3,0,0,1,3,0,0],[0,0,0,3,0,1,1,3,0,0],[0,0,0,3,3,3,3,2,0,0],[0,0,0,3,3,3,2,2,0,0],[1,0,0,0,0,0,0,0,0,0],[2,3,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,5,5,5,5,4,4],[0,0,0,0,5,5,5,5,5,4],[0,0,0,0,5,1,1,3,5,5],[0,0,0,0,5,1,3,3,5,5],[0,0,0,0,5,3,3,3,5,5],[0,0,0,0,5,3,3,3,5,5],[0,0,0,0,5,3,3,1,5,5],[0,1,3,0,4,3,1,1,5,5],[0,4,5,0,4,4,5,5,5,5],[0,0,0,0,0,0,0,0,0,0]],
    [[3,3,5,5,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,5,3,3,3,3,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,5,5,3,3,3,3,3,3,3,3,3],[3,3,3,3,2,2,9,9,9,9,9,9,9,9,3,3,3],[3,3,3,3,2,9,9,9,9,9,9,9,9,9,3,3,3],[3,3,3,3,9,9,9,6,6,1,1,9,9,2,3,3,3],[3,3,3,3,9,9,9,6,6,6,1,9,2,2,3,3,3],[3,3,3,3,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,1,6,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,2,9,3,3,3,6,6,6,6,3,3,3,3,3,3],[3,3,4,0,3,3,3,1,6,6,6,3,3,3,3,3,3],[3,3,8,9,3,3,3,1,1,6,6,3,3,3,3,3,3]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,4],[0,0,0,0,0,0,6,6,7,7,7,0,4,4,4,4,4,4],[0,0,0,0,0,0,6,7,7,7,7,0,0,0,0,0,0,0],[0,0,0,0,0,0,7,7,7,7,7,0,0,0,0,0,0,0],[3,3,0,0,0,0,7,7,7,7,6,0,0,0,6,6,0,0],[6,7,0,0,0,0,7,7,7,6,6,0,0,0,6,6,0,0],[4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[7,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
]

results = []
for i, (input_grid, output_grid) in enumerate(zip(train_inputs, train_outputs)):
    input_np = np.array(input_grid)
    output_np = np.array(output_grid)

    bg_color = find_background_color(input_np)
    sources, source_coords = get_source_pixels(input_np, bg_color)
    inferred_map = infer_mapping(input_np, output_np, bg_color, sources, source_coords)
    inferred_fill_colors = set(inferred_map.values())

    # Calculate observed fill colors directly for comparison
    mask = (input_np == bg_color)
    fill_colors_observed = set(output_np[mask]) - {bg_color} if np.any(mask) else set()

    results.append({
        "Example": i + 1,
        "Background (BG)": bg_color,
        "Sources (S)": sorted(list(sources)),
        "Inferred Map (S->F)": inferred_map,
        "Inferred Fill Colors (F)": sorted(list(inferred_fill_colors)),
        "Observed Fill Colors": sorted(list(fill_colors_observed)),
        "Map Correctly Predicts Observed Fills": inferred_fill_colors == fill_colors_observed
    })

# Pretty print results using the converter
print(json.dumps(convert_numpy_types(results), indent=2))