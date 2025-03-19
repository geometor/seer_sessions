import numpy as np

def is_solid_color_line(line):
    """Checks if a line (list) contains only one unique non-zero value."""
    unique_values = np.unique(line)
    return len(unique_values) == 1 and unique_values[0] != 0

def analyze_task(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        input_solid_lines = []
        for i, row in enumerate(input_grid):
            if is_solid_color_line(row):
                input_solid_lines.append((i, row.tolist()))
        
        output_solid_lines = []
        for i, row in enumerate(output_grid):
            if is_solid_color_line(row):
                output_solid_lines.append((i, row.tolist()))

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'input_solid_lines': input_solid_lines,
            'output_solid_lines': output_solid_lines,
            'output_width_match_first_example' : output_grid.shape[1] == task['train'][0]['output'].shape[1]
        })
    return results

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[3, 3, 3, 3, 3, 3, 3, 3]]
        }
    ]
}

analysis_results = analyze_task(task)
for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Input shape: {result['input_shape']}")
    print(f"  Output shape: {result['output_shape']}")
    print(f"  Input solid lines (index, line): {result['input_solid_lines']}")
    print(f"  Output solid lines (index, line): {result['output_solid_lines']}")
    print(f"  Output width match first example: {result['output_width_match_first_example']}")
    print("-" * 30)