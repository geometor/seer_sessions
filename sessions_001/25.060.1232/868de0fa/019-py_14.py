import numpy as np

# Example data (replace with actual data from the task)
# I am creating simplified examples to demonstrate the concept

# these have been simplified from the training set examples
example_inputs = [
    np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]),
    np.array([[1, 1, 1, 1], [1, 0, 0, 1], [1, 1, 1, 1]]),
    np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]])
]

example_outputs = [
    np.array([[1, 1, 1], [1, 7, 1], [1, 1, 1]]),
    np.array([[1, 1, 1, 1], [1, 7, 7, 1], [1, 1, 1, 1]]),
    np.array([[7, 7, 7, 7], [7, 1, 1, 7], [7, 7, 7, 7]])
]

previous_code_outputs = [
    np.array([[1, 1, 1], [1, 7, 1], [1, 1, 1]]),
    np.array([[1, 1, 1, 1], [1, 7, 7, 1], [1, 1, 1, 1]]),
    np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]])
]


def calculate_metrics(input_grid, expected_output, actual_output):
    """Calculates metrics for a single example."""

    input_white_count = np.sum(input_grid == 0)
    input_blue_count = np.sum(input_grid == 1)
    expected_orange_count = np.sum(expected_output == 7)
    actual_orange_count = np.sum(actual_output == 7)
    correct_pixels = np.sum(expected_output == actual_output)
    total_pixels = expected_output.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0

    return {
        "input_white": int(input_white_count),
        "input_blue": int(input_blue_count),
        "expected_orange": int(expected_orange_count),
        "actual_orange": int(actual_orange_count),
        "accuracy": float(accuracy),
    }

for i, (inp, exp, act) in enumerate(zip(example_inputs, example_outputs, previous_code_outputs)):
    metrics = calculate_metrics(inp, exp, act)
    print(f"Example {i+1} Metrics: {metrics}")
