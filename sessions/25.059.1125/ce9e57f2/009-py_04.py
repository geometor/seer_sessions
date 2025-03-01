import numpy as np

def analyze_results(examples):
    analysis = []
    for idx, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        actual_output_grid = transform(input_grid) # Use your transform function from above.

        input_red_count = np.sum(input_grid == 2)
        expected_output_red_count = np.sum(expected_output_grid == 2)
        actual_output_red_count = np.sum(actual_output_grid == 2)
        
        input_rows, input_cols = input_grid.shape

        red_pixel_changes = []

        rows, cols = input_grid.shape
        for i in range(rows):
          for j in range(cols):
            if input_grid[i,j] == 2 and expected_output_grid[i,j] == 8:
              red_pixel_changes.append( (i,j) )
        
        analysis.append({
            'example_index': idx,
            'input_shape': input_grid.shape,
            'input_red_pixels': input_red_count.item(),  # Use .item() for scalar values
            'expected_output_red_pixels': expected_output_red_count.item(),
            'actual_output_red_pixels': actual_output_red_count.item(),
            'red_pixel_change_locations': red_pixel_changes,
            'correct': np.array_equal(expected_output_grid, actual_output_grid)
        })

    return analysis

# Paste the examples from the task here
examples = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 2, 0, 0], [0, 0, 0, 2, 0, 0, 2, 0, 0], [0, 0, 0, 2, 0, 0, 2, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 2, 0, 0], [0, 0, 0, 8, 0, 0, 8, 0, 0], [0, 0, 0, 8, 0, 0, 8, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 8, 0, 0, 0], [0, 0, 8, 0, 0, 0]]}
]

analysis_results = analyze_results(examples)
print(analysis_results)
