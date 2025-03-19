def show_grids(grid1, grid2):
    print("Grid 1:")
    print(grid1)
    print("\nGrid 2:")
    print(grid2)

example_data = task_data['train']
num_examples = len(example_data)
results = []

for i in range(num_examples):
  input_grid = np.array(example_data[i]['input'])
  expected_output = np.array(example_data[i]['output'])
  actual_output = transform(input_grid)  # Use the provided transform function
  comparison = np.array_equal(actual_output,expected_output)
  print(f"example {i}:")
  show_grids(input_grid,expected_output)
  print(f"comparison: {comparison}")
  results.append(comparison)

print(results)
