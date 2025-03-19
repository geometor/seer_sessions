import numpy as np

def compare_grids(input_grid, expected_output, actual_output):
    """Compares the input, expected output, and actual output grids."""

    print("Input Grid:")
    print(input_grid)
    print("\nExpected Output Grid:")
    print(expected_output)
    print("\nActual Output Grid:")
    print(actual_output)
    print("-" * 20)

# Example data from Task (replace with actual data)

example_data = [
    {
      "input": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [8, 1, 1, 1, 8], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [3, 1, 1, 1, 3]],
      "output": [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [8, 3, 3, 3, 8], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 6, 3, 3, 3]],
    },
    {
      "input": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [8, 1, 1, 1, 8], [8, 1, 1, 1, 8], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [3, 1, 1, 1, 3]],
      "output": [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [8, 3, 3, 3, 8], [8, 3, 3, 3, 8], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 6, 3, 3, 3]],
    },
    {
      "input": [[8, 1, 1, 1, 8], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [8, 1, 1, 1, 8]],
      "output": [[8, 3, 3, 3, 8], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [8, 3, 3, 3, 8]],
    },
    {
        "input": [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [8, 1, 1, 1, 8], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
        "output": [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [8, 3, 3, 3, 8], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3]],
    },
        {
        "input": [[8, 1, 1, 1, 8], [8, 1, 1, 1, 8], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [8, 1, 1, 1, 8], [8, 1, 1, 1, 8], [3, 1, 1, 1, 3]],
        "output": [[8, 3, 3, 3, 8], [8, 3, 3, 3, 8], [3, 3, 3, 3, 3], [3, 3, 3, 3, 3], [8, 3, 3, 3, 8], [8, 3, 3, 3, 8], [3, 6, 3, 3, 3]],
    }
]

for i, example in enumerate(example_data):
    actual_output = transform(np.array(example["input"]))
    print(f"Example {i + 1}:")
    compare_grids(np.array(example["input"]), np.array(example["output"]), actual_output)