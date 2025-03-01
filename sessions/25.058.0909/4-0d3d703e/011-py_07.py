def code_execution():
    results = []
    for task in train_tasks: # Assuming 'train_tasks' is accessible
      input_grid = np.array(task['input'])
      expected_output_grid = np.array(task['output'])
      actual_output_grid = transform(input_grid)

      input_dims = input_grid.shape
      output_dims = expected_output_grid.shape
      input_colors = np.unique(input_grid).tolist()
      output_colors = np.unique(expected_output_grid).tolist()
      input_color_counts = {color: np.sum(input_grid == color) for color in input_colors}
      output_color_counts = {color: np.sum(expected_output_grid == color) for color in output_colors}
      pixel_diff = np.sum(expected_output_grid != actual_output_grid)

      results.append({
          'input_dims': input_dims,
          'output_dims': output_dims,
          'input_colors': input_colors,
          'output_colors': output_colors,
          'input_color_counts': input_color_counts,
          'output_color_counts': output_color_counts,
          'pixel_diff': pixel_diff
      })
    return results

code_execution_results = code_execution()
print(code_execution_results)