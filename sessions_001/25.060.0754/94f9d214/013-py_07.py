import numpy as np

def analyze_results(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_grid = transform(example['input'])
        match = np.array_equal(output_grid, predicted_grid)

        results.append({
            'example': i + 1,
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'predicted_shape': np.array(predicted_grid).shape,
            'input_colors': np.unique(input_grid).tolist(),
            'output_colors': np.unique(output_grid).tolist(),
            'predicted_colors': np.unique(predicted_grid).tolist(),
            'match': match
        })
    return results

# Assuming 'task' variable holds the task data as provided
# Replace with the actual task structure
# I will make a mock because the environment did not provide it
# but this is my task to do next
task = {
  "train": [
    {
      "input": [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0, 0]
      ],
      "output": [
        [2, 2, 0],
        [2, 2, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 8, 8],
        [0, 0, 0, 0, 8, 8],
        [0, 0, 0, 0, 8, 8],
        [0, 0, 0, 0, 8, 8]
      ],
      "output": [
        [0, 0, 2],
        [0, 0, 2]
      ]
    },
      {
      "input": [
        [6, 6, 6, 6, 1, 1],
        [6, 6, 6, 6, 1, 1],
        [6, 6, 0, 0, 1, 1],
        [6, 6, 0, 0, 1, 1]
      ],
      "output": [
        [2, 0, 0],
        [0, 0, 0]
      ]
    }
  ]
}

analysis = analyze_results(task['train'])

for result in analysis:
    print(result)
