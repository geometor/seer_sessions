def transform(inp):
    # make the output the same as input
    out = inp.copy()
    return out
import numpy as np

task_json = {
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
            "output": [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
        },
         {
            "input": [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
            "output": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1],[1, 1, 1, 1, 1]],
        },
        {
            "input": [[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8]],
            "output": [[8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8]],
        },
    ]
}
def code_execution(input_grid, output_grid, expected_output):
    """
    Simulates code execution and provides metrics.  In a real environment,
    this would involve running code against NumPy arrays.
    """

    correct_pixels = np.sum(output_grid == expected_output)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    report = {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "expected_output_shape": expected_output.shape,
        "accuracy": accuracy,
        "notes": ""
    }
    if input_grid.shape != expected_output.shape:
        report["notes"] = "Input and expected output shapes differ."

    return report

# example data (replace with actual data)
example_reports = []
for i in range(len(task_json['train'])):
  input_grid = np.array(task_json['train'][i]['input'])
  output_grid = transform(input_grid)
  expected_output = np.array(task_json['train'][i]['output'])
  example_reports.append(code_execution(input_grid, output_grid, expected_output))

for i, report in enumerate(example_reports):
    print(f"--- Example {i+1} ---")
    for key, value in report.items():
        print(f"{key}: {value}")