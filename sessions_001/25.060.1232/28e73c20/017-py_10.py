import numpy as np

def analyze_grids(task_data):
    results = {}
    for example_type in ['train', 'test']:
        if example_type in task_data:
            results[example_type] = []
            for i, example in enumerate(task_data[example_type]):
                input_grid = np.array(example['input'])
                output_grid = np.array(example['output'])

                input_dims = input_grid.shape
                output_dims = output_grid.shape
                input_colors = np.unique(input_grid).tolist()
                output_colors = np.unique(output_grid).tolist()

                results[example_type].append({
                    'input_dims': input_dims,
                    'output_dims': output_dims,
                    'input_colors': input_colors,
                    'output_colors': output_colors,
                    'example_number': i +1
                })
    return results

#Dummy task data for example execution (replace with the real data passed in previously)
task_data = {
    'train': [
        {'input': [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 'output': [[3, 3, 3], [3, 3, 3], [3, 3, 3]]},
        {'input': [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 'output': [[3, 3, 3], [3, 1, 3], [3, 3, 3]]},
        {'input': [[5, 5], [5, 5]], 'output': [[3, 3], [3, 3]]}
    ]
}

analysis_results = analyze_grids(task_data)
print(analysis_results)