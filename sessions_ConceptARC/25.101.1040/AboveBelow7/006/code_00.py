import numpy as np
from collections import defaultdict

# --- Helper Function ---
def get_color_group_properties(grid: np.ndarray) -> dict:
    rows, cols = grid.shape
    color_groups = defaultdict(lambda: {'coords': set(), 'min_r': rows, 'max_r': -1, 'min_c': cols, 'max_c': -1})
    found_non_background = False
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                found_non_background = True
                group = color_groups[color]
                group['coords'].add((r, c))
                group['min_r'] = min(group['min_r'], r)
                group['max_r'] = max(group['max_r'], r)
                group['min_c'] = min(group['min_c'], c)
                group['max_c'] = max(group['max_c'], c)
    if not found_non_background: return {}
    result = {}
    for color, group_data in color_groups.items():
         result[color] = {
             'coords': group_data['coords'],
             'coords_count': len(group_data['coords']), # Add count
             'bbox': (group_data['min_r'], group_data['max_r'], group_data['min_c'], group_data['max_c'])
         }
    return result

# --- Transformation Function (from previous correct code) ---
def transform_function(input_grid: list[list[int]]) -> list[list[int]]:
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    output_array = np.zeros_like(input_array)
    color_groups = get_color_group_properties(input_array)
    if len(color_groups) != 2: return input_grid # Return original if not 2 colors
    colors = list(color_groups.keys())
    color1, color2 = colors[0], colors[1]
    group1, group2 = color_groups[color1], color_groups[color2]
    if group1['bbox'][0] < group2['bbox'][0]:
        upper_group, lower_group = group1, group2
        upper_color, lower_color = color1, color2
    else:
        upper_group, lower_group = group2, group1
        upper_color, lower_color = color2, color1
    upper_min_r, upper_max_r, _, _ = upper_group['bbox']
    lower_min_r, lower_max_r, _, _ = lower_group['bbox']
    gap = lower_min_r - upper_max_r - 1
    for r, c in lower_group['coords']:
        if 0 <= r < rows and 0 <= c < cols: output_array[r, c] = lower_color
    new_upper_group_start_row = lower_max_r + gap + 1
    shift = new_upper_group_start_row - upper_min_r
    for r, c in upper_group['coords']:
        new_r = r + shift
        if 0 <= new_r < rows and 0 <= c < cols: output_array[new_r, c] = upper_color
    return output_array.tolist()

# --- Train 1 Data & Analysis ---
train_1_input_list = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0],[0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0],[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0],[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0],[0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
train_1_expected_list = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0],[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0],[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0],[0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0]
]
transformed_1_list = transform_function(train_1_input_list)
print("--- Train 1 Metrics ---")
print(f"Match Expected: {np.array_equal(transformed_1_list, train_1_expected_list)}")

# --- Train 2 Data & Analysis ---
train_2_input_list = [
    [0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 8, 0, 0, 0, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 8, 8, 8, 0],
    [0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0], [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0], [0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
train_2_expected_list = [ # From Prompt
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0], [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 0, 0, 0, 2, 0, 2, 2, 2, 0], [0, 2, 2, 2, 2, 2, 2, 0, 0, 8, 0, 0],
    [0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 8, 0], [0, 0, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
transformed_2_list = transform_function(train_2_input_list)
transformed_2_np = np.array(transformed_2_list)
expected_2_np = np.array(train_2_expected_list)
input_2_np = np.array(train_2_input_list)

print("\n--- Train 2 Metrics ---")
props_in_2 = get_color_group_properties(input_2_np)
props_exp_2 = get_color_group_properties(expected_2_np)
props_trans_2 = get_color_group_properties(transformed_2_np)

colors_2 = list(props_in_2.keys())
color_map_2 = {8: 'Azure', 2: 'Red'}
c1, c2 = colors_2[0], colors_2[1]
n1, n2 = color_map_2.get(c1, str(c1)), color_map_2.get(c2, str(c2))

print(f"Input Counts: {n1}={props_in_2[c1]['coords_count']}, {n2}={props_in_2[c2]['coords_count']}")
print(f"Input BBoxes: {n1}={props_in_2[c1]['bbox']}, {n2}={props_in_2[c2]['bbox']}")
print(f"Expected Counts: {n1}={props_exp_2.get(c1, {}).get('coords_count', 0)}, {n2}={props_exp_2.get(c2, {}).get('coords_count', 0)}")
print(f"Expected BBoxes: {n1}={props_exp_2.get(c1, {}).get('bbox', None)}, {n2}={props_exp_2.get(c2, {}).get('bbox', None)}")
print(f"Transformed Counts: {n1}={props_trans_2.get(c1, {}).get('coords_count', 0)}, {n2}={props_trans_2.get(c2, {}).get('coords_count', 0)}")
print(f"Transformed BBoxes: {n1}={props_trans_2.get(c1, {}).get('bbox', None)}, {n2}={props_trans_2.get(c2, {}).get('bbox', None)}")

# Compare Transformed vs Expected
diff = transformed_2_np != expected_2_np
pixels_off = np.sum(diff)
print(f"\nMatch Expected: False")
print(f"Pixels Off (Transformed vs Expected): {pixels_off}")
print("Differences (Row, Col): TransformedValue vs ExpectedValue")
diff_indices = np.where(diff)
count = 0
for r, c in zip(*diff_indices):
    print(f"({r}, {c}): {transformed_2_np[r,c]} vs {expected_2_np[r,c]}", end="; ")
    count += 1
    if count % 4 == 0: print() # Newline every 4 diffs
print("\n(End of Differences)")
