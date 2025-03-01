import numpy as np

def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        #find rows in input that contains 5 white pixels
        input_rows_with_5_white = np.where((input_grid == 0).sum(axis=1) == 5)[0]
        
        #find rows in output that contains 5 white pixels
        output_rows_with_5_white = np.where((output_grid == 0).sum(axis=1) == 5)[0]
        
        #find rows in output that contains 2 blue pixels
        output_rows_with_2_blue = np.where((output_grid == 1).sum(axis=1) == 2)[0]
        
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'input_rows_with_5_white': input_rows_with_5_white.tolist(),
            'output_rows_with_5_white': output_rows_with_5_white.tolist(),
            'output_rows_with_2_blue' : output_rows_with_2_blue.tolist(),
        })
    return results

# this is where I would load data from a json file if run locally
task_data = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5]
      ],
      "output": [
        [1, 0, 0, 0, 1],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5]
      ]
    },
    {
      "input": [
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5]
      ],
      "output": [
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [1, 0, 0, 0, 1],
        [5, 5, 5, 5, 5]
      ]
    },
    {
      "input": [
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [0, 0, 0, 0, 0]
      ],
      "output": [
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [1, 0, 0, 0, 1]
      ]
    }
  ]
}

analysis = analyze_results(task_data)

for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Input Rows with 5 White: {result['input_rows_with_5_white']}")
    print(f"  Output Rows with 5 White: {result['output_rows_with_5_white']}")
    print(f"  Output Rows with 2 Blue: {result['output_rows_with_2_blue']}")
    print("-" * 20)