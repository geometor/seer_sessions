import numpy as np
import json # Use json for better printing of complex structures

# --- Function to calculate metrics (same as provided before) ---
def analyze_example(input_grid_list, expected_output_list, transformed_output_list):
    input_grid = np.array(input_grid_list)
    expected_output = np.array(expected_output_list)
    transformed_output = np.array(transformed_output_list)

    metrics = {}
    # Grid properties
    metrics['height'] = input_grid.shape[0]
    metrics['width'] = input_grid.shape[1]

    # Color analysis
    shape_colors = set(input_grid[input_grid > 0])
    metrics['distinct_shape_colors'] = sorted([int(c) for c in shape_colors]) # Ensure serializable ints
    metrics['num_distinct_shape_colors'] = len(shape_colors)

    # Comparison results
    match = np.array_equal(expected_output, transformed_output)
    metrics['match'] = bool(match) # Ensure serializable bool
    if not match:
        metrics['pixels_off'] = int(np.sum(expected_output != transformed_output)) # Ensure serializable int
        # Identify mismatch locations and values
        diff_indices = np.where(expected_output != transformed_output)
        mismatches = []
        for r, c in zip(*diff_indices):
            mismatches.append({
                'location': (int(r), int(c)),
                'expected': int(expected_output[r, c]),
                'transformed': int(transformed_output[r, c])
            })
        metrics['mismatches'] = mismatches
    else:
        metrics['pixels_off'] = 0
        metrics['mismatches'] = []

    return metrics

# --- Data for Example 1 ---
grid1_in = [
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 2, 0, 0, 0, 0, 0, 0], [0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0]
]
grid1_out_expected = [
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 2, 3, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 3, 2, 0, 0, 0, 0, 0, 0], [0, 2, 3, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
    [0, 0, 0, 4, 7, 7, 7, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0]
]
# Transformed output from Code v3 as reported in failure log
grid1_out_transformed = [
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 2, 0, 0, 0, 0, 0, 0], [0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 4, 0, 0], [0, 0, 0, 4, 4, 4, 4, 4, 0, 0]
]

# --- Data for Example 2 ---
grid2_in = [
    [0,0,0,0,0,0,0,0,0,0,0,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,4,0,4],
    [0,0,0,0,0,0,0,0,0,0,0,4,0,4],[0,2,2,2,2,2,2,2,2,0,0,4,0,4],
    [0,2,0,0,0,0,0,0,2,0,0,4,0,4],[0,2,0,0,0,0,0,0,2,0,0,4,4,4],
    [0,2,2,2,2,2,2,2,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,7,7,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,0,7],[0,0,7,7,7,7,7,7,7,0,0,7,0,7],
    [0,0,7,0,0,0,0,0,7,0,0,7,0,7],[0,0,7,7,7,7,7,7,7,0,0,7,0,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,0,7],[0,0,0,0,0,0,0,0,0,0,0,7,7,7]
]
grid2_out_expected = [
    [0,0,0,0,0,0,0,0,0,0,0,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,4,3,4],
    [0,0,0,0,0,0,0,0,0,0,0,4,3,4],[0,2,2,2,2,2,2,2,2,0,0,4,3,4],
    [0,2,7,7,7,7,7,7,2,0,0,4,3,4],[0,2,7,7,7,7,7,7,2,0,0,4,4,4],
    [0,2,2,2,2,2,2,2,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,7,7,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,3,7],[0,0,7,7,7,7,7,7,7,0,0,7,3,7],
    [0,0,7,0,0,0,0,0,7,0,0,7,3,7],[0,0,7,7,7,7,7,7,7,0,0,7,3,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,3,7],[0,0,0,0,0,0,0,0,0,0,0,7,7,7]
]
# Transformed output from Code v3 as reported in failure log
grid2_out_transformed = [
    [0,0,0,0,0,0,0,0,0,0,0,4,4,4],[0,0,0,0,0,0,0,0,0,0,0,4,0,4],
    [0,0,0,0,0,0,0,0,0,0,0,4,0,4],[0,2,2,2,2,2,2,2,2,0,0,4,0,4],
    [0,2,0,0,0,0,0,0,2,0,0,4,0,4],[0,2,0,0,0,0,0,0,2,0,0,4,4,4],
    [0,2,2,2,2,2,2,2,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,7,7,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,0,7],[0,0,7,7,7,7,7,7,7,0,0,7,0,7],
    [0,0,7,0,0,0,0,0,7,0,0,7,0,7],[0,0,7,7,7,7,7,7,7,0,0,7,0,7],
    [0,0,0,0,0,0,0,0,0,0,0,7,0,7],[0,0,0,0,0,0,0,0,0,0,0,7,7,7]
]

# --- Calculate and print metrics ---
metrics1 = analyze_example(grid1_in, grid1_out_expected, grid1_out_transformed)
metrics2 = analyze_example(grid2_in, grid2_out_expected, grid2_out_transformed)

print("--- Example 1 Metrics (Code v3) ---")
print(json.dumps(metrics1, indent=2))

print("\n--- Example 2 Metrics (Code v3) ---")
print(json.dumps(metrics2, indent=2))
