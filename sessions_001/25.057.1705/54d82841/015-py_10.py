def get_column_colors(grid, col_index):
    """Returns a sorted list of unique colors in a given column."""
    return sorted(list(np.unique(grid[:, col_index])))

def analyze_examples(task_data):
   results = []
   for example in task_data['train']:
      input_grid = np.array(example['input'])
      output_grid = np.array(example['output'])
      predicted_output = transform(input_grid)
      correct = np.array_equal(predicted_output,output_grid)
      
      analysis = {
          'example_id': example.get('id', 'N/A'), # Use .get() in case 'id' is missing
          'input_shape': input_grid.shape,
          'output_shape': output_grid.shape,
          'correct' : correct,
          'column_analysis': []
      }
      
      for col_index in range(input_grid.shape[1]):
         column_colors = get_column_colors(input_grid, col_index)
         output_pixel = output_grid[-1, col_index]
         analysis['column_analysis'].append({
             'column_index': col_index,
             'colors': column_colors,
             'output_pixel': output_pixel
         })
      results.append(analysis)
   return results
task_data = {
    "train": [
        {
            "input": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            "output": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [4, 4, 4]],
            "id": "train_0",
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "output": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 4, 4, 4]],
            "id": "train_1",
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 8, 0, 0]],
            "output": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 8, 0, 0], [0, 4, 4, 4]],
            "id": "train_2",
        },
    ],
    "test": [{"input": [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "output": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [4, 4, 4]]}],
}

analysis_results = analyze_examples(task_data)
print(analysis_results)
