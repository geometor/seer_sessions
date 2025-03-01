import numpy as np

def analyze_examples(task_data):
    results = []
    for example in task_data['train']: #only train
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        #find the blue line
        blue_line_coords = np.where(output_grid == 1)
        blue_line_cols = blue_line_coords[1]
        if len(blue_line_cols) > 0:
            blue_line_col = blue_line_cols[0] #all should be in same column
        else:
            blue_line_col = -1 #no blue line

        #find the red lines - coordinates and lengths
        red_line_coords = np.where(output_grid == 2)
        red_line_data = []
        if len(red_line_coords[0])> 0:
            unique_cols = np.unique(red_line_coords[1])
            for col in unique_cols:
                rows = red_line_coords[0][red_line_coords[1] == col]
                red_line_data.append({
                    'col': col,
                    'start_row': np.min(rows),
                    'end_row': np.max(rows),
                    'length': np.max(rows) - np.min(rows) + 1
                })
        
        results.append({
            'blue_line_col': blue_line_col,
            'red_lines': red_line_data,
            'input_grid': input_grid.tolist(),
            'output_grid': output_grid.tolist()
        })
    return results

task_data = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 5, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 2, 0, 0, 1, 0, 0, 0, 0], [0, 2, 0, 0, 1, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 5, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 2, 0], [0, 0, 0, 0, 1, 0, 0, 2, 0], [0, 0, 0, 0, 1, 0, 0, 2, 0]]},
        {'input': [[0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 4, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 2, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0]]},
        {'input': [[5, 0, 0, 0, 5, 0, 0, 0, 5], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 4, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0]], 'output': [[2, 0, 0, 0, 1, 0, 0, 0, 2], [2, 0, 0, 0, 1, 0, 0, 0, 0], [2, 0, 0, 0, 1, 0, 2, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0]]}
    ]
}

analysis = analyze_examples(task_data)
print(analysis)
