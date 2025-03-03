import numpy as np

def calculate_metrics(input_grid, expected_output_grid, actual_output_grid):
    input_array = np.array(input_grid)
    expected_output_array = np.array(expected_output_grid)
    actual_output_array = np.array(actual_output_grid)

    metrics = {
        "input_dimensions": input_array.shape,
        "expected_output_dimensions": expected_output_array.shape,
        "actual_output_dimensions": actual_output_array.shape,
        "input_colors": np.unique(input_array, return_counts=True),
        "expected_output_colors": np.unique(expected_output_array, return_counts=True),
        "actual_output_colors": np.unique(actual_output_array, return_counts=True),
        "is_rotation_correct": np.array_equal(np.rot90(input_array), actual_output_array),
        "is_output_correct": np.array_equal(expected_output_array, actual_output_array)
    }
    return metrics

input_grid = [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
expected_output_grid = [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
actual_output_grid = [[1, 0, 0], [1, 0, 0], [1, 0, 0]] # Assuming the current code's output

metrics = calculate_metrics(input_grid, expected_output_grid, actual_output_grid)
print(metrics)
