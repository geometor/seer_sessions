import numpy as np

def describe_grid(grid, name):
    grid = np.array(grid)
    non_zero_pixels = np.sum(grid != 0)
    height, width = grid.shape
    print(f"Grid: {name}")
    print(f"  Dimensions: {width}x{height}")
    print(f"  Non-white Pixels: {non_zero_pixels}")
    if non_zero_pixels > 0:
      min_row, max_row, min_col, max_col = get_bounding_box(grid)
      print(f"Bounding Box: Top={min_row}, Bottom={max_row}, Left={min_col}, Right={max_col}")
    else:
      print("  Bounding Box: None (empty grid)")
    print()

#Example data (Assuming this is loaded elsewhere in the real setup)
training_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0]],
        "output": [[1]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[3]]
    },
     {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[3]]
    },
    {
        "input":  [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        "output": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
    }
]

for i, example in enumerate(training_examples):
  describe_grid(example["input"], f"Training Example {i+1} - Input")
  describe_grid(example["output"], f"Training Example {i+1} - Output")
