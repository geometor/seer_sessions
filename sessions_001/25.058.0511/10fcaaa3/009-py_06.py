import numpy as np

def analyze_results(examples, transform_function):
  results = []
  for i, example in enumerate(examples):
    input_grid = np.array(example['input'])
    expected_output = np.array(example['output'])
    predicted_output = transform_function(input_grid)
    
    correct = np.array_equal(expected_output, predicted_output)

    input_height, input_width = input_grid.shape
    output_height, output_width = expected_output.shape
    
    metrics = {
      'example_index': i,
      'correct': correct,
      'input_shape': (input_height, input_width),
      'output_shape': (output_height, output_width),
      'output_equals_predicted': np.array_equal(expected_output, predicted_output)
    }
    results.append(metrics)

  return results

# This assumes you have 'train' defined as the list of training examples
# Replace with your actual data structure if different
# Here's a placeholder, assuming your 'task' variable exists and has the train examples:
task = { 'train': [
    {'input': [[1]], 'output': [[1, 1], [1, 1]]},
    {'input': [[1, 2], [3, 4]], 'output': [[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]]},
    {'input': [[5, 6, 7]], 'output': [[5, 5, 6, 6, 7, 7], [5, 5, 6, 6, 7, 7]]},
]
}

results = analyze_results(task['train'], transform)
for result in results:
    print(result)
