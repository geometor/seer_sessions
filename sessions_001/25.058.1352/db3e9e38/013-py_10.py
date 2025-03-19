import numpy as np

def analyze_grid(grid, grid_name):
    rows, cols = grid.shape
    orange_pixels = np.sum(grid == 7)
    azure_pixels = np.sum(grid == 8)
    print(f"{grid_name} - Shape: ({rows}, {cols}), Orange Pixels: {orange_pixels}, Azure Pixels: {azure_pixels}")

# Example data (replace with actual data from the task)
examples = [
    {"input": np.array([[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 0, 0]]),
     "output": np.array([[0, 0, 0, 0, 7, 0],
                         [0, 0, 0, 8, 7, 0],
                         [0, 0, 7, 0, 7, 0],
                         [0, 8, 0, 0, 7, 0],
                         [7, 0, 0, 0, 7, 0],
                         [0, 0, 0, 0, 0, 0]])},

    {"input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 7, 0, 0, 0, 0, 0, 0],
                        [0, 7, 0, 0, 0, 0, 0, 0],
                        [0, 7, 0, 0, 0, 0, 0, 0],
                        [0, 7, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]]),
     "output": np.array([[0, 7, 0, 0, 0, 0, 0, 0],
                         [8, 7, 0, 0, 0, 0, 0, 0],
                         [7, 0, 0, 0, 0, 0, 0, 0],
                         [8, 0, 0, 0, 0, 0, 0, 0],
                         [7, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0]])},

    {"input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 0, 0, 0, 7, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     "output": np.array([[0, 0, 0, 0, 0, 0, 0, 7, 0],
                         [0, 0, 0, 0, 0, 0, 8, 7, 0],
                         [0, 0, 0, 0, 0, 7, 0, 7, 0],
                         [0, 0, 0, 0, 8, 0, 0, 7, 0],
                         [0, 0, 0, 7, 0, 0, 0, 7, 0],
                         [0, 0, 8, 0, 0, 0, 0, 7, 0],
                         [0, 7, 0, 0, 0, 0, 0, 0, 0]])},
    {"input": np.array([[7, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0]]),
    "output" : np.array([[7, 8, 7, 8, 7, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]])
    }
]

for i, example in enumerate(examples):
  analyze_grid(example["input"], f"Example {i+1} Input")
  analyze_grid(example["output"], f"Example {i+1} Output")

  # add analysis of the transform result
  output_grid = transform(example["input"])
  analyze_grid(output_grid, f"Example {i+1} Result")
  print("matches:", np.array_equal(output_grid, example["output"]))
  print("---")