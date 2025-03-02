import numpy as np

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        input_shape = input_grid.shape
        output_shape = output_grid.shape

        input_nonzero_indices = np.where(input_grid != 0)
        output_nonzero_indices = np.where(output_grid != 0)

        #get the actual values from the input
        input_nonzero_value = -1
        if input_nonzero_indices[0].size > 0 and input_nonzero_indices[1].size > 0:
            input_nonzero_value = input_grid[input_nonzero_indices[0][0], input_nonzero_indices[1][0]]

        results.append({
            'input_shape': input_shape,
            'output_shape': output_shape,
            'input_nonzero_indices': input_nonzero_indices,
            'input_nonzero_value': input_nonzero_value,
            'output_nonzero_indices': output_nonzero_indices
        })
    return results

# the task variable is assumed to be in scope from the larger notebook
task = {
    'train': [
        {'input': [[0, 0, 0, 0, 2]], 'output': [[0, 0, 0, 0, 2], [0, 0, 0, 2, 0], [0, 0, 2, 0, 0], [0, 2, 0, 0, 0], [2, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 6, 0]], 'output': [[0, 0, 0, 6, 0], [0, 0, 6, 0, 0], [0, 6, 0, 0, 0], [6, 0, 0, 0, 0], [0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 1]], 'output': [[0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0], [0, 0, 0], [0, 3, 0], [0, 0, 0]], 'output': [[0, 0, 0, 0], [0, 3, 0, 0], [3, 0, 0, 0], [0, 0, 0, 0]]}
    ]
}

analysis_results = analyze_examples(task)
print(analysis_results)