import numpy as np

# Helper function to display grids
def display_grid(grid, title="Grid"):
    print(f"\n--- {title} ---")
    print(grid)


# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
        "output": np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
    },
    {
        "input": np.array([[5, 5, 5, 5], [5, 5, 5, 5], [5, 1, 5, 5]]),
        "output": np.array([[2, 5, 5, 5], [5, 5, 5, 5], [5, 1, 5, 5]]),
    },
    {
        "input": np.array([[1, 5, 5], [5, 5, 5], [5, 5, 5]]),
        "output": np.array([[2, 5, 5], [5, 5, 5], [5, 5, 5]]),
    },
        {
        "input": np.array([[5, 5, 1], [5, 5, 5], [5, 5, 5]]),
        "output": np.array([[2, 5, 1], [5, 5, 5], [5, 5, 5]]),
    },
    {
        "input": np.array([[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
        "output": np.array([[2, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
    },
]

results = []

for i, example in enumerate(examples):
  input_grid = example['input']
  output_grid = example['output']
  predicted_grid = np.copy(input_grid)
  if np.any(input_grid == 1):
      predicted_grid[0, 0] = 2
  result = np.array_equal(predicted_grid, output_grid)
  results.append(result)
  print(f"Example {i + 1}: {result}")
  display_grid(input_grid, "Input")
  display_grid(output_grid, "Output")
  display_grid(predicted_grid, "Predicted")

print(results)
