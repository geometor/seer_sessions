import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    """Analyzes a single example and provides metrics."""

    correct = np.array_equal(output_grid, predicted_output)

    print(f"  Correct: {correct}")
    print(f"  Input:\n{input_grid}")
    print(f"  Expected Output:\n{output_grid}")
    print(f"  Predicted Output:\n{predicted_output}")
    if not correct:
        diff = output_grid != predicted_output
        print(f"  Differences:\n{diff}")
        print(f"output_grid[diff] = {output_grid[diff]}")
        print(f"predicted_output[diff] = {predicted_output[diff]}")

def consolidated_analysis(task):
    for i, example in enumerate(task['train']):
        print(f"Example {i+1}:")
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid.copy())
        analyze_example(input_grid, output_grid, predicted_output)