import numpy as np

def analyze_results(input_grid, expected_output, predicted_output):
    input_5_count = np.sum(input_grid == 5)
    expected_5_count = np.sum(expected_output == 5)
    predicted_5_count = np.sum(predicted_output == 5)

    expected_8_count = np.sum(expected_output == 8)
    predicted_8_count = np.sum(predicted_output == 8)
    diff = predicted_output - expected_output

    correct_pixels = np.sum(predicted_output == expected_output)
    total_pixels = expected_output.size
    accuracy = correct_pixels / total_pixels if total_pixels else 0

    metrics = {
        'input_5s': int(input_5_count),
        'expected_5s': int(expected_5_count),
        'predicted_5s': int(predicted_5_count),
        'expected_8s': int(expected_8_count),
        'predicted_8s': int(predicted_8_count),
        'accuracy': float(accuracy),
        'diff_pixels': diff.tolist()
    }
    return metrics

# example 0 - works perfectly
example0_input = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
example0_output = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])

# run previous transform function
predicted_output0 = transform(example0_input)

# example 1
example1_input = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
example1_output = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 5, 8, 5, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
predicted_output1 = transform(example1_input)

# example 2
example2_input = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
example2_output = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])

predicted_output2 = transform(example2_input)

metrics0 = analyze_results(example0_input, example0_output, predicted_output0)
metrics1 = analyze_results(example1_input, example1_output, predicted_output1)
metrics2 = analyze_results(example2_input, example2_output, predicted_output2)

print("Metrics for Example 0:", metrics0)
print("Metrics for Example 1:", metrics1)
print("Metrics for Example 2:", metrics2)