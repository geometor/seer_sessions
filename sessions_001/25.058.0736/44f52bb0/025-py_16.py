import numpy as np

def analyze_grid(grid, grid_name):
    dimensions = grid.shape
    unique, counts = np.unique(grid, return_counts=True)
    value_counts = dict(zip(unique, counts))
    print(f"Analysis of {grid_name}:")
    print(f"  Dimensions: {dimensions}")
    print(f"  Pixel Value Counts: {value_counts}")

task_data = {
    "train": [
        {
            "input": np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
            "output": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        },
        {
            "input": np.array([[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]]),
            "output": np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]),
        },
        {
            "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8]]),
            "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        },
        {
            "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
            "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        },
    ]
}

for example_index, example in enumerate(task_data["train"]):
  print(f"Example {example_index + 1}:")
  analyze_grid(example["input"], "input")
  analyze_grid(example["output"], "output")
  print("-" * 20)