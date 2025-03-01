import numpy as np

def count_replaced_pixels(input_grid, output_grid):
    return np.sum((input_grid == 0) & (output_grid == 3))

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        replaced_count = count_replaced_pixels(input_grid, output_grid)
        results.append({
            'replaced_count': replaced_count,
            'input_white_count': np.sum(input_grid == 0),
            'output_green_count': np.sum(output_grid == 3)

        })
    return results