import numpy as np

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]]),
    },
    {
        "input": np.array([[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        "output": np.array([[0, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]),
        "output": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0]]),
    }
]

def get_grid_dimensions(grid):
  return grid.shape

for i, example in enumerate(examples):
  input_dims = get_grid_dimensions(example["input"])
  output_dims = get_grid_dimensions(example["output"])
  print(f"Example {i+1}: Input Dimensions = {input_dims}, Output Dimensions = {output_dims}")