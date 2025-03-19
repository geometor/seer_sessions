import numpy as np

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        unique_colors_input = np.unique(input_grid[input_grid != 0])
        num_unique_colors_input = len(unique_colors_input)

        output_shape = output_grid.shape
        unique_colors_output = np.unique(output_grid[output_grid != 0])
        num_unique_colors_output = len(unique_colors_output)
        
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_shape,
            'unique_colors_input': unique_colors_input.tolist(),
            'num_unique_colors_input': num_unique_colors_input,
            'unique_colors_output': unique_colors_output.tolist(),
            'num_unique_colors_output': num_unique_colors_output,

        })
    return results

#this is standin for the 'task' provided by ARC
task_data = {
    'train': [
        {'input': [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0]], 'output': [[1, 2, 0], [0, 0, 0], [0, 0, 0]]},
        {'input': [[0, 7, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 6, 0, 0]], 'output': [[7, 6], [0, 0]]},
        {'input': [[5, 0, 0], [0, 0, 0], [0, 0, 9]], 'output': [[5, 9]]}
    ]
}

analysis = analyze_examples(task_data)

for index, item in enumerate(analysis):
    print(f"Example: {index}")
    print(item)