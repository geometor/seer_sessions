def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)
        is_correct = np.array_equal(predicted_output_grid, expected_output_grid)

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': expected_output_grid.shape,
            'predicted_output_shape': predicted_output_grid.shape,
            'correct': is_correct,
            'first_incorrect_pixel': find_first_difference(expected_output_grid, predicted_output_grid) if not is_correct else None,

        })
    return results

def find_first_difference(grid1, grid2):
    """Find the first pixel where two grids differ."""
    size = grid1.shape
    for i in range(size[0]):
      for j in range(size[1]):
          if grid1[i,j] != grid2[i,j]:
            return (i,j)
    return None