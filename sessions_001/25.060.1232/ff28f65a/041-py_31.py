import numpy as np

def analyze_grids(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        input_shape = input_grid.shape
        output_shape = output_grid.shape
        row_ratio = input_shape[0] / output_shape[0]
        col_ratio = input_shape[1] / output_shape[1]
        results.append({
            'input_shape': input_shape,
            'output_shape': output_shape,
            'row_ratio': row_ratio,
            'col_ratio': col_ratio
        })
    return results

# Assuming the 'task' variable from ARC is available
# For demonstration, let's simulate a task with a couple examples
task = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0], [0, 0, 2, 2, 2, 0, 0], [0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0], [0, 1, 0], [0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 2, 0], [0, 0, 0, 0, 0]], 'output': [[0, 0], [0, 1]]},
        {'input': [[0,0,0,0,0,0],[0,2,0,0,0,0],[0,0,0,0,0,0],[0,0,0,2,2,2],[0,0,0,0,0,0],[0,0,0,0,0,0]], 'output': [[0,0],[0,1]]}
    ]
}

grid_analysis = analyze_grids(task)
print(grid_analysis)