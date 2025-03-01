def analyze_grid_sizes(task):
    results = []
    for example in task['train']:
        input_grid = example['input']
        output_grid = example['output']
        input_height, input_width = len(input_grid), len(input_grid[0])
        output_height, output_width = len(output_grid), len(output_grid[0])
        height_ratio = output_height / input_height
        width_ratio = output_width / input_width
        results.append(
            {
                'input_shape': (input_height, input_width),
                'output_shape': (output_height, output_width),
                'height_ratio': height_ratio,
                'width_ratio': width_ratio
            }
        )
    return results