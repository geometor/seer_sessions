def get_grid_shape(grid):
    return (len(grid), len(grid[0]) if grid else 0)

def check_if_output_is_input_row(input_grid, output_grid):
    if not output_grid or len(output_grid) != 1:
        return -1  # Output is not a single row
    output_row = output_grid[0]
    for i, input_row in enumerate(input_grid):
        if input_row == output_row:
            return i  # Return index of matching row
    return -1 # No match found

task_data = {
    "train": [
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
        },
                {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
        }

    ]
}

results = []
for example in task_data["train"]:
  input_grid = example["input"]
  output_grid = example["output"]
  input_shape = get_grid_shape(input_grid)
  output_shape = get_grid_shape(output_grid)
  row_match = check_if_output_is_input_row(input_grid, output_grid)
  results.append({
      "input_shape": input_shape,
      "output_shape": output_shape,
      "row_match": row_match
  })

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input shape: {result['input_shape']}")
    print(f"  Output shape: {result['output_shape']}")
    print(f"  Output row matches input row: {result['row_match']}")
