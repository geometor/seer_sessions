import numpy as np

def analyze_transformation(input_grid, expected_output, predicted_output):
    """Analyzes the transformation results, comparing expected and predicted outputs."""
    metrics = {
        "total_red_input": np.sum(input_grid == 2),
        "total_red_output": np.sum(expected_output == 2),
        "transformed": np.sum((input_grid == 2) & (expected_output == 4)),
        "correct_change": np.sum((predicted_output == 4) & (expected_output == 4) & (input_grid == 2)),
        "incorrect_change": np.sum((predicted_output == 4) & (expected_output != 4) & (input_grid == 2)),
        "missed_changes": np.sum((predicted_output == 2) & (expected_output == 4) & (input_grid == 2)),
    }
    return metrics

# Example usage (replace with actual data from the task)
task_data = [
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 2, 2, 2, 8, 8, 8],
                           [8, 8, 8, 2, 2, 2, 8, 8, 8],
                           [8, 8, 8, 2, 2, 2, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 4, 2, 4, 8, 8, 8],
                            [8, 8, 8, 2, 2, 2, 8, 8, 8],
                            [8, 8, 8, 4, 2, 4, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 2, 2, 2, 8, 8, 8],
                           [8, 8, 2, 8, 2, 8, 8, 8],
                           [8, 8, 2, 2, 2, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 4, 2, 4, 8, 8, 8],
                            [8, 8, 2, 8, 2, 8, 8, 8],
                            [8, 8, 4, 2, 4, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8]]),
    },
  {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 2, 8, 8, 8],
                           [8, 8, 2, 2, 2, 8, 8],
                           [8, 8, 8, 2, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 2, 8, 8, 8],
                            [8, 8, 2, 2, 2, 8, 8],
                            [8, 8, 8, 2, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8]]),
    },
    {
        "input": np.array([[2, 2, 2, 8, 8, 8, 8, 8],
                           [2, 2, 2, 8, 8, 8, 8, 8],
                           [2, 2, 2, 8, 8, 8, 2, 2],
                           [8, 8, 8, 8, 8, 8, 2, 2],
                           [8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[4, 2, 4, 8, 8, 8, 8, 8],
                            [2, 2, 2, 8, 8, 8, 8, 8],
                            [4, 2, 4, 8, 8, 8, 4, 4],
                            [8, 8, 8, 8, 8, 8, 4, 4],
                            [8, 8, 8, 8, 8, 8, 8, 8]]),
    },
]

results = []
for i, example in enumerate(task_data):
  predicted_output = transform(example["input"])
  metrics = analyze_transformation(example["input"], example["output"], predicted_output)
  results.append(metrics)
  print(f"Example {i+1}:")
  print(metrics)
