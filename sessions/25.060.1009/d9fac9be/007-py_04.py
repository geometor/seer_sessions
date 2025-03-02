# This is a HYPOTHETICAL representation of how code_execution would be used.
# The actual module is not available in this environment.

def analyze_results(task_data, transform_function):
  """
  Analyzes the results of applying a transform function to task examples.

  Args:
    task_data: dict containing 'train' and 'test' examples.
    transform_function: the transformation function.

  Returns:
    A dictionary of metrics.
  """
  metrics = {}
  for set_name, examples in task_data.items():
        metrics[set_name] = []
        for i, example in enumerate(examples):
            input_grid = example['input']
            expected_output = example['output']
            predicted_output = transform_function(input_grid)
            
            discontiguous_red_count_input = count_discontiguous_red_pixels(np.array(input_grid)) #count single red cells
            discontiguous_red_count_output = count_discontiguous_red_pixels(np.array(expected_output))#count single red cells
            correct_size = np.array(expected_output).shape == predicted_output.shape
            
            metrics[set_name].append({
                'example_index': i,
                'input_shape': np.array(input_grid).shape,
                'expected_output_shape': np.array(expected_output).shape,
                'predicted_output_shape': predicted_output.shape,
                'discontiguous_red_count_input' : discontiguous_red_count_input,
                'discontiguous_red_count_output' : discontiguous_red_count_output,               
                'correct_size': correct_size
            })

  return metrics

import json

task_data = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0], [0, 0]]}
    ],
    'test': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0], [0, 0]]}
   ]
}

metrics = analyze_results(task_data, transform)
print(json.dumps(metrics, indent=2))
