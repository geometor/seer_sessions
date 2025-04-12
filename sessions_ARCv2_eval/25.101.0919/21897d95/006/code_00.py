import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

# Helper functions
def _find_background_mask(grid: np.ndarray) -> np.ndarray:
    h, w = grid.shape
    if h == 0: return np.zeros((h, w), dtype=bool)
    bottom_row_colors = set(grid[h - 1, :])
    if not bottom_row_colors: return np.zeros((h, w), dtype=bool)
    potential_bg_mask = np.isin(grid, list(bottom_row_colors))
    structure = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=bool) # 8-way
    labeled_potential_bg, num_labels = label(potential_bg_mask, structure=structure)
    labels_touching_bottom = set(labeled_potential_bg[h - 1, :])
    if 0 in labels_touching_bottom: labels_touching_bottom.remove(0)
    if not labels_touching_bottom: return np.zeros((h, w), dtype=bool)
    background_mask = np.isin(labeled_potential_bg, list(labels_touching_bottom))
    return background_mask

# --- Data --- (Same as previous execution)
examples = {
    "train_1": {
        "input": np.array([
            [6, 6, 6, 6, 6, 7, 7, 7, 4, 4, 4, 4], [6, 6, 6, 6, 6, 7, 7, 7, 4, 4, 4, 4],
            [6, 6, 6, 1, 6, 7, 7, 7, 4, 4, 4, 4], [6, 6, 6, 3, 1, 7, 7, 7, 4, 9, 9, 9],
            [6, 6, 6, 1, 6, 7, 7, 7, 4, 4, 4, 9], [6, 6, 6, 6, 6, 7, 7, 7, 4, 4, 4, 9],
            [6, 6, 6, 6, 6, 7, 1, 7, 4, 4, 4, 4], [6, 6, 6, 6, 6, 7, 1, 1, 4, 4, 4, 4],
            [6, 6, 6, 6, 6, 7, 1, 7, 4, 4, 4, 4], [6, 6, 6, 6, 6, 7, 7, 7, 4, 4, 4, 4],
            [7, 7, 1, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 1, 0, 1, 7, 7, 7, 7, 7, 1, 1, 1],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 1, 7], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
        ]),
        "output": np.array([
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3, 3, 3, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3, 3, 3, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3, 3, 3, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 3, 3, 3, 7, 7, 7],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 7, 7], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 7, 7],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 7, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 7, 7, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 7, 7, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 7, 7, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 7, 7, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 7, 7, 7]
        ])
    },
     "train_2": {
        "input": np.array([
            [7, 7, 7, 7, 7, 7, 1, 7, 3, 3], [7, 7, 7, 7, 7, 7, 1, 1, 3, 3],
            [7, 7, 7, 7, 7, 7, 1, 7, 3, 3], [8, 8, 8, 3, 1, 7, 7, 7, 3, 1],
            [8, 8, 8, 1, 1, 7, 7, 7, 1, 6], [8, 1, 8, 3, 1, 7, 7, 7, 3, 1],
            [8, 1, 1, 3, 3, 1, 9, 1, 3, 3], [8, 1, 8, 3, 3, 7, 1, 7, 3, 3],
            [8, 8, 8, 3, 3, 5, 5, 5, 3, 3], [8, 8, 8, 3, 3, 5, 5, 5, 3, 3]
        ]),
        "output": np.array([
            [6, 6, 6, 6, 6, 6, 6, 6, 7, 7], [6, 6, 6, 6, 6, 6, 6, 6, 7, 7],
            [6, 6, 6, 6, 6, 6, 6, 6, 7, 7], [3, 3, 3, 8, 8, 6, 6, 6, 7, 7],
            [3, 3, 3, 8, 8, 6, 6, 6, 7, 7], [3, 3, 3, 8, 8, 6, 6, 6, 7, 7],
            [3, 3, 3, 8, 8, 6, 6, 6, 7, 7], [3, 3, 3, 8, 8, 6, 6, 6, 7, 7],
            [3, 3, 3, 8, 8, 9, 9, 9, 7, 7], [3, 3, 3, 8, 8, 9, 9, 9, 7, 7]
        ])
    },
     "train_3": {
         "input": np.array([
            [6, 6, 6, 3, 1, 3, 3, 3, 3], [6, 6, 6, 1, 1, 3, 3, 3, 3],
            [6, 6, 6, 3, 1, 3, 3, 3, 3], [6, 6, 6, 4, 4, 4, 4, 1, 4],
            [6, 6, 6, 4, 4, 4, 1, 1, 1], [6, 6, 6, 4, 4, 4, 4, 4, 4],
            [6, 6, 6, 6, 1, 6, 4, 4, 4], [6, 6, 6, 6, 1, 1, 4, 4, 4],
            [6, 6, 6, 6, 1, 6, 4, 4, 4], [5, 5, 5, 4, 4, 4, 4, 4, 4],
            [9, 9, 9, 8, 8, 8, 8, 8, 8], [9, 5, 5, 8, 8, 8, 1, 7, 1],
            [9, 5, 5, 8, 8, 8, 8, 1, 8], [5, 5, 5, 4, 4, 4, 4, 4, 4]
        ]),
        "output": np.array([
            [5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3], [5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3], [7, 8, 8, 8, 6, 3, 3, 3, 6, 6, 6, 4, 4, 4],
            [7, 8, 8, 8, 6, 3, 3, 3, 6, 6, 6, 4, 4, 4], [7, 8, 8, 8, 6, 3, 3, 3, 6, 6, 6, 4, 4, 4],
            [7, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4], [7, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4],
            [7, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4]
        ])
    },
    "train_4": {
        "input": np.array([
            [2, 2, 2, 2, 2, 1, 2, 3, 3, 3], [2, 2, 2, 2, 2, 1, 1, 3, 3, 3],
            [2, 2, 2, 2, 2, 1, 2, 3, 3, 3], [6, 6, 6, 6, 1, 6, 6, 3, 1, 3],
            [6, 6, 6, 1, 1, 1, 6, 1, 1, 3], [1, 1, 1, 6, 6, 6, 6, 3, 1, 3],
            [6, 1, 6, 6, 6, 6, 6, 3, 3, 3], [4, 4, 4, 4, 4, 4, 4, 3, 3, 3],
            [4, 4, 4, 4, 4, 4, 4, 3, 3, 3], [4, 4, 4, 4, 4, 4, 4, 3, 3, 3]
        ]),
        "output": np.array([
            [6, 6, 6, 6, 6, 6, 6, 2, 2, 2], [6, 6, 6, 6, 6, 6, 6, 2, 2, 2],
            [6, 6, 6, 6, 6, 6, 6, 2, 2, 2], [3, 3, 3, 3, 3, 3, 3, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 2, 2, 2], [3, 3, 3, 3, 3, 3, 3, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 2, 2, 2], [6, 6, 6, 6, 6, 6, 6, 2, 2, 2],
            [6, 6, 6, 6, 6, 6, 6, 2, 2, 2], [6, 6, 6, 6, 6, 6, 6, 2, 2, 2]
        ])
    }
}

analysis_log = []
master_map_S_O = {} # Global S -> O map

for name, data in examples.items():
    analysis_log.append(f"--- Analyzing {name} ---")
    input_grid = data["input"]
    expected_output = data["output"]
    h_in, w_in = input_grid.shape
    h_out, w_out = expected_output.shape

    # Analyze Background
    bg_mask = _find_background_mask(input_grid)
    expected_bg_color = -1
    bg_coords_in = np.argwhere(bg_mask)
    if bg_coords_in.size > 0:
        r_in_sample, c_in_sample = bg_coords_in[0]
        r_out_sample = c_in_sample
        c_out_sample = h_in - 1 - r_in_sample
        if 0 <= r_out_sample < h_out and 0 <= c_out_sample < w_out:
             expected_bg_color = expected_output[r_out_sample, c_out_sample]
        else:
             if h_out > 0 and w_out > 0 : expected_bg_color = expected_output[-1,-1] # Fallback guess
    analysis_log.append(f"  Observed Expected Output BG Color: {expected_bg_color}")

    # Analyze Foreground Regions
    fg_mask = ~bg_mask
    # Label foreground regions based on COLOR first
    labeled_fg_by_color, num_fg_labels_color = label(input_grid * fg_mask)
    objects_by_color = find_objects(labeled_fg_by_color) # Get slices for each label

    processed_labels = set()
    structure = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=bool) # 8-way

    analysis_log.append("  FG Mappings Found (S = FG Colors in BBox -> O = Output Color):")
    # Iterate through potential labels found by color
    for i in range(num_fg_labels_color):
        label_idx = i + 1 # Labels are 1-based
        if label_idx in processed_labels: continue

        # Get coordinates for this specific occurrence
        coords = np.argwhere(labeled_fg_by_color == label_idx)
        if coords.size == 0: continue
        
        # Find the full connected component this label belongs to, based on its color
        region_color = input_grid[coords[0,0], coords[0,1]]
        color_mask = (input_grid == region_color) & fg_mask # Mask for this color in foreground
        labeled_components, num_components = label(color_mask, structure=structure)

        # Identify the specific component label for our current coords[0]
        current_component_label = labeled_components[coords[0,0], coords[0,1]]
        if current_component_label == 0: continue

        # Process this specific connected component fully
        component_mask = (labeled_components == current_component_label)
        
        # Mark all original color-based labels within this component as processed
        unique_labels_in_component = np.unique(labeled_fg_by_color[component_mask])
        for ul in unique_labels_in_component:
             if ul > 0: processed_labels.add(ul)

        component_coords = np.argwhere(component_mask)
        if component_coords.size == 0: continue

        # Calculate bounding box for this component
        min_r, min_c = component_coords.min(axis=0)
        max_r, max_c = component_coords.max(axis=0)
        bbox_slice = (slice(min_r, max_r + 1), slice(min_c, max_c + 1))

        # Get all FOREGROUND pixels within the bounding box
        bbox_pixels = input_grid[bbox_slice]
        bbox_fg_mask = fg_mask[bbox_slice]
        bbox_fg_pixels = bbox_pixels[bbox_fg_mask]
        
        # Signal S = frozenset of unique FOREGROUND colors in the bounding box
        S = frozenset(np.unique(bbox_fg_pixels))

        # Find corresponding output color O by sampling a point from the component
        r_in_sample, c_in_sample = component_coords[0]
        r_out_sample = c_in_sample
        c_out_sample = h_in - 1 - r_in_sample

        output_color_O = -1
        if 0 <= r_out_sample < h_out and 0 <= c_out_sample < w_out:
            output_color_O = expected_output[r_out_sample, c_out_sample]
        else:
             analysis_log.append(f"    WARN: Sampled FG coords invalid in output for {name}, region color {region_color}")
             continue

        analysis_log.append(f"    - Region Color {region_color}: S={str(set(S))} -> O={output_color_O}")

        # Store/update the global map, logging conflicts
        if S in master_map_S_O:
            if master_map_S_O[S] != output_color_O:
                analysis_log.append(f"      CONFLICT DETECTED for S={str(set(S))}: Existing O={master_map_S_O[S]}, New O={output_color_O} (from {name}). Overwriting.")
                master_map_S_O[S] = output_color_O
        else:
            master_map_S_O[S] = output_color_O

# Print combined log
print("\n".join(analysis_log))

print("\n--- Final Derived Master Foreground Map (S -> O) ---")
# Sort by set size then content for readability
sorted_map_items = sorted(master_map_S_O.items(), key=lambda item: (len(item[0]), sorted(list(item[0]))))
final_map_dict = {str(sorted(list(k))): v for k, v in sorted_map_items}
print(final_map_dict)

# Try to find a rule for Background Color
bg_analysis = {}
for name, data in examples.items():
     input_grid = data["input"]
     h_in, w_in = input_grid.shape
     bg_mask = _find_background_mask(input_grid)
     bg_coords_in = np.argwhere(bg_mask)
     expected_bg_color = -1
     if bg_coords_in.size > 0:
        r_in_sample, c_in_sample = bg_coords_in[0]
        r_out_sample = c_in_sample
        c_out_sample = h_in - 1 - r_in_sample
        if 0 <= r_out_sample < data["output"].shape[0] and 0 <= c_out_sample < data["output"].shape[1]:
             expected_bg_color = data["output"][r_out_sample, c_out_sample]
     input_bg_colors = tuple(sorted(list(np.unique(input_grid[bg_mask])))) if np.any(bg_mask) else tuple()
     bg_analysis[name] = {'Input BG Colors': input_bg_colors, 'Output BG Color': expected_bg_color}

print("\n--- Background Color Analysis ---")
print(bg_analysis)
# Check if Output BG color matches any value in the master_map_S_O
consistent_bg_rule = True
possible_bg_rule = "Output BG Color = master_map_S_O[frozenset(Input BG Colors)]"
for name, data in bg_analysis.items():
    input_bg_set = frozenset(data['Input BG Colors'])
    expected_output_bg = data['Output BG Color']
    if input_bg_set not in master_map_S_O or master_map_S_O[input_bg_set] != expected_output_bg:
         consistent_bg_rule = False
         print(f"BG Rule Check Fail ({name}): S={set(input_bg_set)}, Expected O={expected_output_bg}, Map gives={master_map_S_O.get(input_bg_set, 'Not Found')}")
         break

if consistent_bg_rule:
     print(f"\nPossible BG Rule Found: {possible_bg_rule}")
else:
     print("\nNo simple BG rule found by mapping Input BG Colors set via the FG map.")
     # Check Min(Input BG Colors) - 1 rule again
     min_minus_one_matches = {}
     for name, data in bg_analysis.items():
         min_val = min(data['Input BG Colors']) if data['Input BG Colors'] else -1
         calc_bg = max(0, min_val - 1) if min_val != -1 else -1
         min_minus_one_matches[name] = (calc_bg == data['Output BG Color'])
     print(f"Min(Input BG)-1 Rule Matches: {min_minus_one_matches}")
     # Check Most Freq Bottom Row Rule again
     most_freq_matches = {}
     for name, data_ex in examples.items():
          input_grid = data_ex["input"]
          h_in, w_in = input_grid.shape
          expected_bg = bg_analysis[name]['Output BG Color']
          calc_bg = -1
          if h_in > 0:
               bottom_row = input_grid[h_in - 1, :]
               if bottom_row.size > 0:
                    colors, counts = np.unique(bottom_row, return_counts=True)
                    calc_bg = colors[np.argmax(counts)]
               else: calc_bg = 0
          else: calc_bg = 0
          most_freq_matches[name] = (calc_bg == expected_bg)
     print(f"Most Freq Bottom Row Rule Matches: {most_freq_matches}")
