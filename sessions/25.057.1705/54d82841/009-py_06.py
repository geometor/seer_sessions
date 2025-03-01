import numpy as np

def analyze_grids(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        input_has_non_white = np.any(input_grid != 0)
        output_has_yellow_bottom_middle = False

        rows, cols = output_grid.shape
        middle_col = cols // 2
        if output_grid[-1, middle_col] == 4:
           output_has_yellow_bottom_middle = True

        results.append({
            'example_index': i,
            'input_has_non_white': bool(input_has_non_white),
            'output_has_yellow_bottom_middle': output_has_yellow_bottom_middle,
            'grids_equal': np.array_equal(input_grid, output_grid)

        })
    return results

examples = [
    {'input': [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 'output': [[0, 0, 0], [0, 0, 0], [0, 4, 0]]},
    {'input': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 4, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]}
]

analysis_results = analyze_grids(examples)
print(analysis_results)