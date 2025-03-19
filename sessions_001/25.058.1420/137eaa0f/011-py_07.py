import numpy as np

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        input_nonzero_count = np.count_nonzero(input_grid)
        output_nonzero_count = np.count_nonzero(output_grid)
        
        input_height, input_width = input_grid.shape
        output_height, output_width = output_grid.shape
        
        input_colors = np.unique(input_grid[input_grid > 0])
        output_colors = np.unique(output_grid[output_grid>0])

        results.append({
            'input_nonzero': input_nonzero_count,
            'output_nonzero': output_nonzero_count,
            'input_shape': (input_height, input_width),
            'output_shape': (output_height, output_width),
            'input_colors': input_colors.tolist(),
            'output_colors': output_colors.tolist(),
            'nonzero_diff': input_nonzero_count - output_nonzero_count
        })
    return results

# Assuming 'task' variable contains the ARC task data
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]],
            "output": [[0, 0, 2], [0, 0, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]],
            "output": [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 3]],
            "output": [[0, 0, 3], [0, 0, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [6, 0, 0, 2]],
            "output": [[6, 0, 2], [0, 0, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 4]],
            "output": [[0, 0, 4], [0, 0, 0], [0, 0, 0]],
        },
    ]
}

analysis_results = analyze_examples(task)
for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Input Non-zero Count: {result['input_nonzero']}")
    print(f"  Output Non-zero Count: {result['output_nonzero']}")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Input Colors: {result['input_colors']}")
    print(f"  Output Colors: {result['output_colors']}")
    print(f"  Non-zero Difference: {result['nonzero_diff']}")
    print("-" * 20)