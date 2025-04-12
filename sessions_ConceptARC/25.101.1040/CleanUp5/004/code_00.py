import numpy as np

# Function to analyze differences (re-used from previous thought process)
def analyze_example(name, input_grid, expected_output_grid, actual_output_grid):
    input_arr = np.array(input_grid)
    expected_arr = np.array(expected_output_grid)
    actual_arr = np.array(actual_output_grid)

    metrics = {}
    metrics['name'] = name
    metrics['input_shape'] = input_arr.shape
    metrics['input_colors'] = sorted(list(np.unique(input_arr)))
    metrics['input_non_white_colors'] = sorted(list(np.unique(input_arr[input_arr != 0])))
    metrics['input_color_count_non_white'] = len(metrics['input_non_white_colors'])

    metrics['expected_output_shape'] = expected_arr.shape
    metrics['expected_output_colors'] = sorted(list(np.unique(expected_arr)))
    metrics['expected_output_non_white_colors'] = sorted(list(np.unique(expected_arr[expected_arr != 0])))

    metrics['actual_output_shape'] = actual_arr.shape
    metrics['actual_output_colors'] = sorted(list(np.unique(actual_arr)))
    metrics['actual_output_non_white_colors'] = sorted(list(np.unique(actual_arr[actual_arr != 0])))

    metrics['match'] = np.array_equal(expected_arr, actual_arr)
    metrics['pixels_off_count'] = int(np.sum(expected_arr != actual_arr)) if not metrics['match'] else 0
    # Get coordinates of differing pixels
    if not metrics['match']:
        diff_coords = np.argwhere(expected_arr != actual_arr)
        metrics['pixels_off_details'] = [(tuple(coord), expected_arr[tuple(coord)], actual_arr[tuple(coord)]) for coord in diff_coords]
    else:
         metrics['pixels_off_details'] = []

    if metrics['input_color_count_non_white'] > 1:
         metrics['max_color_in_input'] = max(metrics['input_non_white_colors']) if metrics['input_non_white_colors'] else None
         metrics['next_max_color_in_input'] = sorted(metrics['input_non_white_colors'])[-2] if len(metrics['input_non_white_colors']) > 1 else None
         metrics['actual_output_contains_max_color'] = metrics['max_color_in_input'] in metrics['actual_output_non_white_colors'] if metrics['max_color_in_input'] else False
         metrics['expected_output_contains_max_color'] = metrics['max_color_in_input'] in metrics['expected_output_non_white_colors'] if metrics['max_color_in_input'] else False
         # Check if actual output matches the simple "remove max color" rule
         temp_output = np.copy(input_arr)
         if metrics['max_color_in_input'] is not None:
             temp_output[temp_output == metrics['max_color_in_input']] = 0
         metrics['actual_matches_simple_remove_max_rule'] = np.array_equal(actual_arr, temp_output)


    return metrics

# Data for train_1
input_1 = [
 [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
 [0, 3, 0, 2, 0, 0, 0, 2, 0, 3, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 3],
 [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0],
 [0, 2, 0, 3, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0],
 [2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
]
# Expected output from task description
expected_1 = [
 [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
 [0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0], # Green (3) at (2,1), (2,9), (2,20) become 0
 [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0], # Green (3) at (3,12), (3,18), (3,19) become 2
 [0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0], # Green (3) at (4,3), (4,15) become 0
 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]  # Green (3) at (5,6) become 0
]
# Actual output from original code (implements simple remove max color rule)
actual_1 = [
 [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
 [0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0], # Removed 3s at (2,1), (2,9), (2,20) -> changed to 0
 [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Removed 3s at (3,12), (3,18), (3,19) -> changed to 0
 [0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0], # Removed 3s at (4,3), (4,15) -> changed to 0
 [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]  # Removed 3 at (5,6) -> changed to 0
]


# Data for train_2
input_2 = [
 [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4],
 [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0],
 [0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0],
 [0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4],
 [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0]
]
expected_2 = [
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0],
 [0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0],
 [0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4],
 [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0]
]
# Actual output from original code (correct for train_2)
actual_2 = [
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0],
 [0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0],
 [0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 4],
 [4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0]
]

metrics_1 = analyze_example("train_1", input_1, expected_1, actual_1)
metrics_2 = analyze_example("train_2", input_2, expected_2, actual_2)

print("--- Metrics Example 1 ---")
for k, v in metrics_1.items():
    print(f"{k}: {v}")

print("\n--- Metrics Example 2 ---")
for k, v in metrics_2.items():
    print(f"{k}: {v}")
