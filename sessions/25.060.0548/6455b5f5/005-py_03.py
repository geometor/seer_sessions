import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    """Analyzes an example and returns a report."""

    report = {
        "input_grid": input_grid.tolist(),
        "expected_output": expected_output.tolist(),
        "actual_output": actual_output.tolist(),
        "differences": (expected_output != actual_output).tolist(),
        "input_colors": np.unique(input_grid).tolist(),
        "expected_colors": np.unique(expected_output).tolist(),
        "actual_colors": np.unique(actual_output).tolist(),

    }
    return report

# Assuming 'train' is a list of dictionaries, each with 'input' and 'output'
train = task["train"]

example_reports = []
for i, example in enumerate(train):
    input_grid = np.array(example['input'])
    expected_output = np.array(example['output'])
    actual_output = transform(input_grid.copy())
    report = analyze_example(input_grid, expected_output, actual_output)
    example_reports.append((i, report))

print(example_reports)