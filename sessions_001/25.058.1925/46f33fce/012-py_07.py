import numpy as np

def calculate_metrics(input_grid, predicted_output_grid, expected_output_grid):
    input_grid = np.array(input_grid)
    predicted_output_grid = np.array(predicted_output_grid)
    expected_output_grid = np.array(expected_output_grid)

    #check if the shapes are equal, and make the smaller one bigger to properly compare
    if(predicted_output_grid.shape != expected_output_grid.shape):
        max_rows = max(predicted_output_grid.shape[0], expected_output_grid.shape[0])
        max_cols = max(predicted_output_grid.shape[1], expected_output_grid.shape[1])
        if(predicted_output_grid.shape[0] < max_rows or predicted_output_grid.shape[1] < max_cols):
            new_predicted = np.zeros((max_rows, max_cols))
            new_predicted[:predicted_output_grid.shape[0], :predicted_output_grid.shape[1]] = predicted_output_grid
            predicted_output_grid = new_predicted
        if(expected_output_grid.shape[0] < max_rows or expected_output_grid.shape[1] < max_cols):
            new_expected = np.zeros((max_rows, max_cols))
            new_expected[:expected_output_grid.shape[0], :expected_output_grid.shape[1]] = expected_output_grid
            expected_output_grid = new_expected

    correct_pixels = np.sum(predicted_output_grid == expected_output_grid)
    total_pixels = predicted_output_grid.size  # Use predicted size to account for potential size differences
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0

    return {
        "input_shape": input_grid.shape,
        "predicted_output_shape": predicted_output_grid.shape,
        "expected_output_shape": expected_output_grid.shape,
        "accuracy": accuracy
    }

def transform(input_grid):
    """
    Transforms the input grid (identity function).
    """
    return input_grid

task_data = [
    {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    }
]

results = []
for example in task_data:
    predicted_output = transform(example["input"])
    metrics = calculate_metrics(example["input"], predicted_output, example["output"])
    results.append(metrics)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Predicted Output Shape: {result['predicted_output_shape']}")
    print(f"  Expected Output Shape: {result['expected_output_shape']}")
    print(f"  Accuracy: {result['accuracy']:.4f}")
    print("-" * 20)