def code_execution(task_id):
    results = []
    for example_type in ['train', 'test']:
        for example_number in range(len(get_task(task_id)[example_type])):
            input_grid = get_task(task_id)[example_type][example_number]['input']
            target_grid = get_task(task_id)[example_type][example_number]['output']
            output_grid = transform(input_grid)
            results.append({
                'example_type': example_type,
                'example_number': example_number,
                'input_shape': np.array(input_grid).shape,
                'output_shape': np.array(output_grid).shape,
                'target_shape': np.array(target_grid).shape,
                'success': output_grid == target_grid,
                'differences': [] if output_grid == target_grid else find_differences(output_grid, target_grid)
            })
    return results

def find_differences(grid1, grid2):
    # simplified diff
    differences = []
    grid1_arr = np.array(grid1)
    grid2_arr = np.array(grid2)

    if grid1_arr.shape != grid2_arr.shape:
        return [("shape_mismatch", grid1_arr.shape, grid2_arr.shape)]

    for row in range(grid1_arr.shape[0]):
      for col in range(grid1_arr.shape[1]):
        if grid1_arr[row, col] != grid2_arr[row, col]:
          differences.append(((row,col), grid1_arr[row, col], grid2_arr[row, col]))
    return differences

# Example Usage (replace 'a85d4709' with the actual task ID):
# Assuming a get_task function is available
results = code_execution('a85d4709')

for result in results:
  if result['success']:
    print(f"Example {result['example_type']} {result['example_number']}: Success")
  else:
    print(f"Example {result['example_type']} {result['example_number']}: Failure")
    print(f"  Input shape: {result['input_shape']}")
    print(f"  Output shape: {result['output_shape']}")
    print(f"  Target shape: {result['target_shape']}")
    print(f"Differences: {result['differences']}")
