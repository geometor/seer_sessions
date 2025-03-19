import numpy as np
from collections import Counter

def analyze_example(input_grid, output_grid, predicted_output):
    """
    Analyzes a single example and provides metrics.
    """
    input_colors = Counter(input_grid.flatten())
    output_colors = Counter(output_grid.flatten())
    predicted_colors = Counter(predicted_output.flatten())

    input_shape = input_grid.shape
    output_shape = output_grid.shape
    predicted_shape = predicted_output.shape

    correct_pixels = np.sum(output_grid == predicted_output)
    total_pixels = output_grid.size
    accuracy = (correct_pixels / total_pixels) * 100 if total_pixels > 0 else 0.0

    return {
        "input_colors": input_colors,
        "output_colors": output_colors,
        "predicted_colors": predicted_colors,
        "input_shape": input_shape,
        "output_shape": output_shape,
        "predicted_shape": predicted_shape,
        "accuracy": accuracy
    }


def test_transform_cases(task_data, transform_func):

    results = []
    for example in task_data:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform_func(input_grid.copy())  # Use a copy to avoid modifying the original
        results.append(analyze_example(input_grid, output_grid, predicted_output))
    return results

# this is replaced in the notebook execution
# task_train = []
# results = test_transform_cases(task_train, transform)

# print(results)
