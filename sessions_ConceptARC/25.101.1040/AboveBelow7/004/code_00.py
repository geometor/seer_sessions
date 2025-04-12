import numpy as np

# --- Input and Expected Output for Train 2 ---
train_2_input = np.array([
    [0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 8, 8, 8, 0, 0, 0, 8, 0, 0],
    [0, 8, 8, 8, 8, 8, 8, 0, 8, 8, 8, 0],
    [0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# Expected output from the failed test report / prompt
train_2_expected_output = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 0, 0, 8, 0, 0], # End of Red Object + Pixel (8,9)=8
    [0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 8, 0], # Row 9
    [0, 0, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], # Row 10
    [0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0], # Row 11
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# --- Helper function to get properties ---
def get_color_group_properties(grid: np.ndarray) -> dict:
    rows, cols = grid.shape
    color_groups = {}
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                if color not in color_groups:
                    color_groups[color] = {'coords': set(), 'min_r': r, 'max_r': r, 'min_c': c, 'max_c': c}
                group = color_groups[color]
                group['coords'].add((r, c))
                group['min_r'] = min(group['min_r'], r)
                group['max_r'] = max(group['max_r'], r)
                group['min_c'] = min(group['min_c'], c)
                group['max_c'] = max(group['max_c'], c)
    result = {}
    for color, group in color_groups.items():
         result[color] = {
             'coords_count': len(group['coords']),
             'bbox': (group['min_r'], group['max_r'], group['min_c'], group['max_c'])
         }
    return result

# --- Calculate and Print Metrics ---
print("--- Train 2 Metrics ---")
props_in = get_color_group_properties(train_2_input)
props_expected = get_color_group_properties(train_2_expected_output)

colors = list(props_in.keys())
color_map = {8: 'Azure', 2: 'Red'} # Assuming these are the colors
color1, color2 = colors[0], colors[1]
name1, name2 = color_map.get(color1, str(color1)), color_map.get(color2, str(color2))

print(f"Input Color Groups: {name1}({color1}): Count={props_in[color1]['coords_count']}, BBox={props_in[color1]['bbox']}; {name2}({color2}): Count={props_in[color2]['coords_count']}, BBox={props_in[color2]['bbox']}")
print(f"Expected Output Color Groups: {name1}({color1}): Count={props_expected[color1]['coords_count']}, BBox={props_expected[color1]['bbox']}; {name2}({color2}): Count={props_expected[color2]['coords_count']}, BBox={props_expected[color2]['bbox']}")

# Determine Upper/Lower
if props_in[color1]['bbox'][0] < props_in[color2]['bbox'][0]:
    upper_color, lower_color = color1, color2
    upper_props, lower_props = props_in[color1], props_in[color2]
else:
    upper_color, lower_color = color2, color1
    upper_props, lower_props = props_in[color2], props_in[color1]

print(f"Identified Upper Group: {color_map.get(upper_color, str(upper_color))}({upper_color}), Lower Group: {color_map.get(lower_color, str(lower_color))}({lower_color})")

# Calculate Gap and Expected Shifted BBox for Upper Group
gap = lower_props['bbox'][0] - upper_props['bbox'][1] - 1
calc_shifted_upper_min_r = lower_props['bbox'][1] + gap + 1
calc_shifted_upper_max_r = calc_shifted_upper_min_r + (upper_props['bbox'][1] - upper_props['bbox'][0])
calc_shifted_upper_bbox = (calc_shifted_upper_min_r, calc_shifted_upper_max_r, upper_props['bbox'][2], upper_props['bbox'][3])

print(f"Calculated Vertical Gap: {gap}")
print(f"Calculated Shifted BBox for Upper Group ({color_map.get(upper_color, str(upper_color))} {upper_color}): {calc_shifted_upper_bbox}")
print(f"Actual Expected BBox for Upper Group ({color_map.get(upper_color, str(upper_color))} {upper_color}): {props_expected[upper_color]['bbox']}")
print(f"Actual Expected BBox for Lower Group ({color_map.get(lower_color, str(lower_color))} {lower_color}): {props_expected[lower_color]['bbox']}")
print(f"Lower Group BBox Unchanged? {props_in[lower_color]['bbox'] == props_expected[lower_color]['bbox']}")
print(f"Pixel Counts Preserved? {props_in[upper_color]['coords_count'] == props_expected[upper_color]['coords_count'] and props_in[lower_color]['coords_count'] == props_expected[lower_color]['coords_count']}")
