# Example of gathering more detailed metrics for each example.
# For each example in the training and test sets:
#   1. Count the occurrences of each color in the input.
#   2. Count the occurrences of each color in the output.
#   3. Identify the pixels that changed and their original and new values.
# These could then be summarized in YAML format in the next deliverable.
import numpy as np

def detailed_report(grid, title):
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"{title=}")
    print(f"{grid.shape=}")
    print(f"{color_counts=}")
    
def detailed_comparison(input_grid, output_grid, transformed_grid):
    if input_grid.shape != output_grid.shape:
        print("Shapes are different, cannot compare")
        return
    diff_output = input_grid != output_grid
    diff_trans = input_grid != transformed_grid
    
    if np.any(diff_output):
        where_diff = np.where(diff_output)
        print("Changes from Input to Output:")
        for i in range(len(where_diff[0])):
            row = where_diff[0][i]
            col = where_diff[1][i]
            print(f"  {row=}, {col=}: {input_grid[row,col]} -> {output_grid[row,col]}")
    else:
        print("Input and Output grids are the same")

    if np.any(diff_trans):
        where_diff = np.where(diff_trans)
        print("Changes from Input to Transformed:")
        for i in range(len(where_diff[0])):
            row = where_diff[0][i]
            col = where_diff[1][i]
            print(f"  {row=}, {col=}: {input_grid[row,col]} -> {transformed_grid[row,col]}")
    else:
        print("Input and Transformed grids are the same")

    show_diff(transformed_grid, output_grid)

for example_index, example in enumerate(task["train"]):
  print (f"\nExample {example_index=}")
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])
  transformed_grid = transform(input_grid)
  detailed_report(input_grid, "INPUT")
  detailed_report(output_grid, "OUTPUT")
  detailed_report(transformed_grid, "TRANSFORMED")
  detailed_comparison(input_grid, output_grid, transformed_grid)
for example_index, example in enumerate(task["test"]):
  print (f"\nTest {example_index=}")
  input_grid = np.array(example["input"])
  transformed_grid = transform(input_grid)
  detailed_report(input_grid, "INPUT")
  detailed_report(transformed_grid, "TRANSFORMED")