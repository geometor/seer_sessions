import numpy as np

def report(grid):
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print (f"{grid.shape=} {color_counts=}")

def show_diff(grid1, grid2):
    if grid1.shape != grid2.shape:
        print("Shapes are different, cannot compare")
        return
    diff = grid1 != grid2
    if np.any(diff):
      print(np.where(diff))
    else:
      print("grids are the same")

task = {
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
            "output": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
        },
        {
            "input": [[5, 0, 5], [0, 5, 0], [5, 0, 5]],
            "output": [[4, 0, 4], [0, 4, 0], [4, 0, 4]],
        },
		{
            "input": [[5, 0, 0], [0, 0, 0], [0, 0, 5]],
            "output": [[4, 0, 0], [0, 0, 0], [0, 0, 4]],
        },
		{
            "input": [[0, 5, 0], [0, 5, 0], [0, 5, 0]],
            "output": [[0, 4, 0], [0, 4, 0], [0, 4, 0]],
        },
        {
            "input": [[0, 0, 0], [0, 5, 0], [0, 0, 0]],
            "output": [[0, 0, 0], [0, 4, 0], [0, 0, 0]],
        },
    ],
    "test": [{"input": [[5, 0, 5], [0, 0, 0], [5, 0, 5]], "output": []}],
}

def transform(input_grid):
    output_grid = np.copy(input_grid)
    output_grid[:] = 4
    return output_grid

for example_index, example in enumerate(task["train"]):
  print (f"\nExample {example_index=}")
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])
  print("INPUT")
  report(input_grid)
  print("OUTPUT")
  report(output_grid)
  transformed_grid = transform(input_grid)
  print("TRANSFORM")
  report(transformed_grid)
  show_diff(transformed_grid, output_grid)