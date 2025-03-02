import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    results = {}

    # Basic size comparison
    results['input_shape'] = input_grid.shape
    results['output_shape'] = output_grid.shape

    # Check for blue in input and output
    results['blue_in_input'] = 1 in input_grid
    results['blue_in_output'] = 1 in output_grid
    if results['blue_in_input']:
      results['blue_input_rows'] = np.where(np.any(input_grid == 1, axis=1))[0].tolist()
    if results['blue_in_output']:
      results['blue_output_rows'] = np.where(np.any(output_grid == 1, axis=1))[0].tolist()    

    # Check for azure (8) in input and output.
    results['azure_in_input'] = 8 in input_grid
    results['azure_in_output'] = 8 in output_grid
    if results['azure_in_input']:
      results['azure_input_rows'] = np.where(np.any(input_grid == 8, axis = 1))[0].tolist()
    if results['azure_in_output']:
      results['azure_output_rows'] = np.where(np.any(output_grid == 8, axis = 1))[0].tolist()
    
    return results

examples = [
    ([[5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5],
      [5, 5, 1, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5]],
     [[0, 8, 8],
      [0, 0, 0],
      [8, 0, 8],
      [0, 0, 0],
      [0, 0, 0]]),
      
      ([[5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 1, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5]],
       [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 8, 8],
        [0, 0, 0],
        [0, 0, 0]]),

      ([[5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 1, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5]],
       [[0, 0, 0],
        [0, 0, 0],
        [8, 0, 8],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]),
        
      ([[5, 5, 5, 5, 5],
        [5, 5, 1, 5, 5],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5],
        [5, 5, 5, 5, 1]],
       [[0, 0, 0],
        [8, 0, 8],
        [0, 0, 0],
        [0, 0, 0],
        [0, 8, 8]])
]

for i, (input_grid, output_grid) in enumerate(examples):
    analysis = analyze_example(input_grid, output_grid)
    print(f"Example {i+1}:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")