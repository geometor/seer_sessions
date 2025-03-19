import numpy as np

def describe_grid(grid):
    """Provides a textual description of the grid."""
    return str(grid)

def compare_grids(expected, actual):
    """Highlights differences between expected and actual grids."""
    return str(expected - actual)

# Example data (replace with actual data from the task)
# These are placeholders;  real data from the ARC task is essential
train_examples = [
  {
        "input": np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]),
        "output": np.array([[1, 1, 1], [1, 0, 1], [1, 4, 1]]),
    },
    {
        "input": np.array([[5, 5, 5, 5], [5, 0, 5, 0], [5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5], [5, 0, 5, 0], [5, 4, 5, 4]]),
    },
    {
      "input": np.array([[5, 5, 5, 5, 5], [5, 0, 5, 0, 5], [5, 5, 5, 5, 5]]),
      "output": np.array([[5, 5, 5, 5, 5], [5, 0, 5, 0, 5], [5, 4, 5, 4, 5]]),
    },
    {
      "input": np.array([[5, 5, 5, 5, 5, 5], [5, 5, 0, 0, 5, 5], [5, 5, 5, 5, 5, 5]]),
      "output": np.array([[5, 5, 5, 5, 5, 5], [5, 5, 0, 0, 5, 5], [5, 5, 4, 4, 5, 5]]),
    },
    {
        "input": np.array([[1, 1, 1], [0, 1, 0], [1, 1, 1]]),
        "output": np.array([[1, 1, 1], [0, 1, 0], [4, 1, 4]]),
    },

]

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(input_grid)

    print(f"--- Example {i+1} ---")
    print("Input:\n", describe_grid(input_grid))
    print("Expected Output:\n", describe_grid(expected_output))
    print("Actual Output:\n", describe_grid(actual_output))
    print("Differences (Expected - Actual):\n", compare_grids(expected_output, actual_output))
    print("\n")
