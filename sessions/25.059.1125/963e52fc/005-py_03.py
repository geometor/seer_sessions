def grid_dims(grid):
    return (len(grid), len(grid[0]))

def compare_grids(grid1, grid2):
    if grid_dims(grid1) != grid_dims(grid2):
        return False
    for i in range(len(grid1)):
        for j in range(len(grid1[0])):
          if grid1[i][j] != grid2[i][j]:
            return False
    return True

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 0], [0, 8, 8, 8, 8, 0], [0, 2, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 0], [0, 8, 8, 8, 8, 0, 8, 8, 8, 8, 0, 0], [0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0], [0, 2, 2, 2, 0], [0, 8, 8, 8, 0], [0, 2, 2, 2, 0], [0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 0, 2, 2, 2, 0, 0], [0, 8, 8, 8, 0, 8, 8, 8, 0, 0], [0, 2, 2, 2, 0, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0], [0, 2, 2, 0], [0, 8, 8, 0], [0, 2, 2, 0], [0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 2, 2, 0, 0], [0, 8, 8, 0, 8, 8, 0, 0], [0, 2, 2, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        }
    ]
}

for i, example in enumerate(task["train"]):
  input_grid = example["input"]
  expected_output = example["output"]
  dims_in = grid_dims(input_grid)
  dims_out = grid_dims(expected_output)
  transformed_grid = transform(input_grid)
  comparison = compare_grids(transformed_grid, expected_output)
  print(f"Example {i+1}:")
  print(f"  Input Dimensions: {dims_in}")
  print(f"  Output Dimensions: {dims_out}")
  print(f"  Transformation Correct: {comparison}")