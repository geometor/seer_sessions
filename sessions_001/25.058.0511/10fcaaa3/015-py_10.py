import numpy as np

def analyze_results(task):
    print(f"Analyzing task: {task['name']}")
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)  # Assuming 'transform' is the provided function

        correct = np.array_equal(predicted_output_grid, expected_output_grid)
        input_shape = input_grid.shape
        output_shape = expected_output_grid.shape
        predicted_output_shape = predicted_output_grid.shape


        results.append({
            "example": example,
            'correct': correct,
            'input_shape': input_shape,
            'output_shape': output_shape,
           'predicted_output_shape': predicted_output_shape
        })
    return results

# the current task - replace this with the actual data structure of your task.
task = {
  'name': "Example Task",
    'train': [
      {
          'input': [[4, 0, 4], [0, 0, 0], [4, 0, 4]],
          'output': [[4, 8, 4, 4, 8, 4], [8, 8, 8, 8, 8, 8], [4, 8, 4, 4, 8, 4]],
      },
      {
          'input': [[0, 4, 0, 0], [0, 0, 0, 0], [0, 4, 0, 4], [0, 0, 0, 0]],
          'output': [[8, 4, 8, 8, 8, 4, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 4, 8, 4, 8, 4, 8, 4], [8, 8, 8, 8, 8, 8, 8, 8]],
      },
      {
            'input':  [[0, 0, 0, 0, 0], [0, 4, 0, 4, 0], [0, 0, 0, 0, 0], [0, 4, 0, 0, 0], [0, 0, 0, 0, 0]],
            'output': [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 4, 8, 4, 8, 8, 4, 8, 4, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
      }
    ]
}
results = analyze_results(task)

for result in results:
  print(result)
