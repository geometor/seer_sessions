def get_metrics(input_grid, expected_output, actual_output):
    import numpy as np
    
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    metrics = {}
    metrics["input_shape"] = input_grid.shape
    metrics["output_shape"] = actual_output.shape
    metrics["match"] = np.array_equal(expected_output, actual_output)
    metrics["different_pixels"] = np.sum(expected_output != actual_output)
    # count number of gray regions
    gray_pixels = input_grid == 5
    metrics["gray_pixel_count"] = np.sum(gray_pixels)

    return metrics

# Example grids (replace with actual data)
example0_input = [[0, 0, 0, 0, 0], [0, 5, 5, 5, 0], [0, 5, 0, 5, 0], [0, 5, 5, 5, 0], [0, 0, 0, 0, 0]]
example0_expected = [[0, 0, 0, 0, 0], [0, 5, 5, 5, 0], [0, 5, 2, 5, 0], [0, 5, 5, 5, 0], [0, 0, 0, 0, 0]]
example0_actual = [[0, 0, 0, 0, 0], [0, 5, 5, 5, 0], [0, 5, 2, 5, 0], [0, 5, 5, 5, 0], [0, 0, 0, 0, 0]]

metrics0 = get_metrics(example0_input, example0_expected, example0_actual)
print(f"Example 0 Metrics: {metrics0}")

example1_input = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
example1_expected = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
example1_actual = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

metrics1 = get_metrics(example1_input, example1_expected, example1_actual)
print(f"Example 1 Metrics: {metrics1}")

example2_input = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 5, 0, 0, 0, 0, 5, 0], [0, 5, 0, 0, 5, 5, 5, 0], [0, 5, 5, 5, 5, 0, 0, 0], [0, 5, 0, 0, 0, 0, 5, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
example2_expected = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 5, 2, 2, 2, 2, 5, 0], [0, 5, 2, 2, 5, 5, 5, 0], [0, 5, 5, 5, 5, 0, 0, 0], [0, 5, 2, 2, 2, 2, 5, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
example2_actual =  [[0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 5, 0, 0, 0, 0, 5, 0], [0, 5, 0, 0, 5, 5, 5, 0], [0, 5, 5, 5, 5, 0, 0, 0], [0, 5, 0, 0, 0, 0, 5, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

metrics2 = get_metrics(example2_input, example2_expected, example2_actual)
print(f"Example 2 Metrics: {metrics2}")