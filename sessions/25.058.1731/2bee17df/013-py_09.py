import numpy as np

def report_execution(input_grid, expected_output, actual_output):
    correct = np.array_equal(expected_output, actual_output)
    input_str = str(input_grid)
    expected_str = str(expected_output)
    actual_str = str(actual_output)

    return f"""
Correct: {correct}
Input:
{input_str}
Expected Output:
{expected_str}
Actual Output:
{actual_str}
"""

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([
            [2, 2, 2, 2, 2],
            [2, 0, 0, 0, 2],
            [2, 0, 0, 0, 2],
            [2, 2, 2, 2, 2]
        ]),
        "output": np.array([
            [2, 2, 2, 2, 2],
            [2, 3, 3, 3, 2],
            [2, 3, 3, 3, 2],
            [2, 2, 2, 2, 2]
        ]),
    },
    {
        "input": np.array([
            [8, 8, 8, 8, 8, 8, 8, 8],
            [8, 0, 8, 0, 8, 0, 0, 8],
            [8, 0, 8, 0, 8, 0, 0, 8],
            [8, 0, 0, 0, 8, 0, 0, 8],
            [8, 8, 8, 8, 8, 8, 8, 8]
        ]),
        "output": np.array([
            [8, 8, 8, 8, 8, 8, 8, 8],
            [8, 0, 8, 0, 8, 0, 0, 8],
            [8, 0, 8, 0, 8, 0, 0, 8],
            [8, 0, 0, 0, 8, 0, 0, 8],
            [8, 8, 8, 8, 8, 8, 8, 8]
        ]),
    },
     {
        "input": np.array([
            [5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 0, 5, 5, 5],
            [5, 5, 0, 0, 0, 5, 5],
            [5, 5, 5, 0, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5]
        ]),
        "output": np.array([
            [5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 3, 5, 5, 5],
            [5, 5, 3, 3, 3, 5, 5],
            [5, 5, 5, 3, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5]
        ]),
    },
  {
        "input": np.array([
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 0, 5, 5, 5, 5],
            [5, 5, 0, 0, 0, 5, 5, 5],
            [5, 5, 5, 0, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5]
        ]),
        "output": np.array([
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 3, 5, 5, 5, 5],
            [5, 5, 3, 3, 3, 5, 5, 5],
            [5, 5, 5, 3, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5]
        ]),
    },
]

for i, example in enumerate(examples):
  actual_output = transform(example["input"])
  print(f"Example {i+1}:")
  print(report_execution(example["input"], example["output"], actual_output))
