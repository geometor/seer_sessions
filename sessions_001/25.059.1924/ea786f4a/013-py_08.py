import numpy as np

def analyze_grids(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        # Find white pixels in input
        input_white_pixels = np.where(input_grid == 0)
        input_white_count = len(input_white_pixels[0])
        input_white_coords = list(zip(input_white_pixels[0].tolist(), input_white_pixels[1].tolist()))
        
        # Find white pixels in output
        output_white_pixels = np.where(output_grid == 0)
        output_white_count = len(output_white_pixels[0])
        output_white_coords = list(zip(output_white_pixels[0].tolist(), output_white_pixels[1].tolist()))

        results.append({
            'input_shape': input_grid.shape,
            'input_white_count': input_white_count,
            'input_white_coords': input_white_coords,
            'output_shape': output_grid.shape,
            'output_white_count': output_white_count,
            'output_white_coords' : output_white_coords
        })
    return results

# Assuming 'task' variable holds the current task data (not provided in the turn, replaced by dummy for illustration)
task = {
    'train': [
        {'input': [[2, 2, 2], [2, 0, 2], [2, 2, 2]], 'output': [[2, 0, 2], [0, 0, 0], [2, 0, 2]]},
        {'input': [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 0, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]], 'output': [[2, 2, 2, 2, 2], [2, 2, 0, 2, 2], [2, 0, 0, 0, 2], [2, 2, 0, 2, 2], [2, 2, 2, 2, 2]]},
        {'input': [[2, 2, 2, 2], [2, 0, 0, 2], [2, 2, 2, 2]], 'output': [[2, 0, 0, 2], [0, 0, 0, 0], [2, 0, 0, 2]]},
        {'input': [[2, 0, 2, 2], [2, 2, 2, 0], [2, 2, 2, 2]], 'output': [[0, 0, 2, 0], [2, 2, 0, 0], [2, 2, 2, 0]]}
    ]
}

analysis_results = analyze_grids(task)
print(analysis_results)
