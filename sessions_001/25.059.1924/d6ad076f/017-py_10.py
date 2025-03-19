def describe_grid(grid):
    rows, cols = grid.shape
    white_region = find_region(grid, 0)
    green_region = find_region(grid, 3)
    maroon_region = find_region(grid, 9)
    azure_region = find_region(grid, 8)


    description = {
        'dimensions': (rows, cols),
        'white_region': white_region,
        'green_region': green_region,
        'maroon_region': maroon_region,
        'azure_region': azure_region,
    }
    return description

def show_example(task, example_number, in_or_out):
  example = task['train'][example_number]
  if in_or_out == "input":
     grid = example['input']
  else:
     grid = example['output']

  grid = np.array(grid)
  return describe_grid(grid)

task = {
    'train': [
        {'input': [[3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [9, 9, 9, 9, 9, 0], [9, 9, 9, 9, 9, 0]], 'output': [[3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 0], [0, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 0], [9, 9, 9, 9, 9, 0], [9, 9, 9, 9, 9, 0]]},
        {'input': [[3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0], [9, 9, 9, 9, 9, 9, 0]], 'output': [[3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 0], [0, 8, 8, 8, 8, 0, 0], [9, 9, 9, 9, 9, 9, 0]]},
        {'input': [[3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [9, 9, 9, 9, 9, 0]], 'output': [[3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 0], [0, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 0], [9, 9, 9, 9, 9, 0]]}
    ]
}

for i in range(3):
  print(f"Example {i}:")
  print(f"  Input: {show_example(task, i, 'input')}")
  print(f"  Output: {show_example(task, i, 'output')}")
