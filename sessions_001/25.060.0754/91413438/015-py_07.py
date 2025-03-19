import numpy as np

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = example['input']
        output_grid = example['output']
        input_np = np.array(input_grid)
        output_np = np.array(output_grid)

        input_shape = input_np.shape
        output_shape = output_np.shape

        # Find blue pixel coordinates (color code 1)
        input_blue_coords = np.argwhere(input_np == 1)
        output_blue_coords = np.argwhere(output_np == 1)

        example_data = {
            'input_shape': input_shape,
            'output_shape': output_shape,
            'input_blue_coords': input_blue_coords.tolist(),
            'output_blue_coords': output_blue_coords.tolist(),
            'tiled_height': output_shape[0],
        }
        results.append(example_data)

    return results