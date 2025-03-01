import numpy as np

def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        # count colors in grids before transformation
        input_counts = {color: 0 for color in range(10)}
        for row in input_grid:
          for pixel in row:
            input_counts[pixel] += 1

        # Count colors in actual output
        output_counts = {color: 0 for color in range(10)}
        for row in output_grid:
          for pixel in row:
            output_counts[pixel] += 1
            
        # run transformation and count colors
        transformed_grid = transform(input_grid)
        transformed_counts = {color: 0 for color in range(10)}
        for row in transformed_grid:
            for pixel in row:
                transformed_counts[pixel] += 1

        results.append({
            'input_counts': input_counts,
            'output_counts': output_counts,
            'transformed_counts': transformed_counts
        })
    return results

# this will be replaced with the actual task data:
example_task_data = {
  "train": [
    {
      "input": [[1, 0, 1], [0, 1, 0], [1, 1, 1]],
      "output": [[2, 0, 2], [0, 2, 0], [2, 2, 2]]
    },
    {
      "input": [[0, 2, 0], [2, 0, 2], [0, 2, 2]],
      "output": [[0, 3, 0], [3, 0, 3], [0, 3, 3]]
    },
     {
      "input": [[3, 0, 0], [0, 0, 0], [0, 0, 3]],
      "output": [[1, 0, 0], [0, 0, 0], [0, 0, 1]]
    }
  ]
}

analysis = analyze_results(example_task_data)

for i, result in enumerate(analysis):
  print(f"Example {i+1}:")
  print(f"   Input Counts: {result['input_counts']}")
  print(f"  Output Counts: {result['output_counts']}")
  print(f"Transf. Counts: {result['transformed_counts']}")
  print("-" * 20)