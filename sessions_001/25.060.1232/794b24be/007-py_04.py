import numpy as np

def describe_grid(grid, grid_name):
    """Provides a description of the grid's properties."""
    print(f"--- {grid_name} ---")
    print(f"Dimensions: {grid.shape}")
    print(f"Unique pixel values: {np.unique(grid)}")
    non_zero_count = np.count_nonzero(grid)
    print(f"Number of non-zero pixels: {non_zero_count}")
    if non_zero_count > 0:
      first_non_zero = np.transpose(np.nonzero(grid))[0]
      print(f"First non-zero pixel at: {first_non_zero} color = {grid[first_non_zero[0],first_non_zero[1]]}")
    print(f"Grid:\n{grid}")

task = {
    "train": [
        {
            "input": np.array([[0, 0, 0], [0, 6, 0], [0, 0, 0]]),
            "output": np.array([[2, 0, 0], [0, 0, 0], [0, 0, 0]]),
        },
        {
            "input": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 8, 0, 0]]),
            "output": np.array([[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        },
         {
            "input": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        },
    ],
     "test": [
        {"input": np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0]]),
         "output": np.array([[2, 0, 0], [0, 0, 0], [0, 0, 0]])},
    ],
}
for example_index, example in enumerate(task["train"]):
  describe_grid(example["input"], f"Example {example_index + 1} Input")
  describe_grid(example["output"], f"Example {example_index + 1} Output")

for example_index, example in enumerate(task["test"]):
  describe_grid(example["input"], f"Test {example_index + 1} Input")
  describe_grid(example["output"], f"Test {example_index + 1} Output")