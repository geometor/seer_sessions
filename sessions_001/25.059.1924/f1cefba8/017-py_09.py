import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    """Analyzes a single example and returns relevant metrics."""

    def get_object_details(grid, color):
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            return None  # Handle case where color is not found
        min_y, min_x = coords.min(axis=0)
        max_y, max_x = coords.max(axis=0)
        height = max_y - min_y + 1
        width = max_x - min_x + 1
        return {
            'top_left': (min_y, min_x),
            'bottom_right': (max_y, max_x),
            'height': height,
            'width': width,
            'size': coords.shape[0]
           }

    input_red = get_object_details(input_grid, 2)
    input_green = get_object_details(input_grid, 3)
    output_red = get_object_details(output_grid, 2)
    output_black = get_object_details(output_grid, 0)
    predicted_black = get_object_details(predicted_output, 0)
    predicted_red = get_object_details(predicted_output, 2)

    return {
        'input_red': input_red,
        'input_green': input_green,
        'output_red': output_red,
        'output_black': output_black,
        'predicted_red': predicted_red,
        'predicted_black' : predicted_black,
        'output_correct': np.array_equal(output_grid, predicted_output)
    }

def calculate_metrics(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid.copy())
        results.append(analyze_example(input_grid, output_grid, predicted_output))
    return results

task = {
    "train": [
        {
            "input": [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 3, 3, 3, 3, 3, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 3, 3, 3, 3, 3, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 3, 3, 3, 3, 3, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 3, 3, 3, 3, 3, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 3, 3, 3, 3, 3, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 3, 3, 3, 3, 3, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]],
            "output": [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 2, 2, 2, 2, 2, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 2, 0, 0, 0, 2, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 2, 0, 0, 0, 2, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 2, 0, 0, 0, 2, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 2, 2, 2, 2, 2, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
        },
        {
            "input": [[2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 7, 7, 7, 2, 2], [2, 2, 2, 2, 7, 3, 7, 2, 2], [2, 2, 2, 2, 7, 7, 7, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2]],
            "output": [[2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 7, 7, 7, 2, 2], [2, 2, 2, 2, 7, 0, 7, 2, 2], [2, 2, 2, 2, 7, 7, 7, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
        },
        {
            "input": [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]],
            "output": [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [2, 2, 2, 7, 0, 0, 0, 0, 0, 0, 0, 7, 2], [2, 2, 2, 7, 0, 0, 0, 0, 0, 0, 0, 7, 2], [2, 2, 2, 7, 0, 0, 0, 0, 0, 0, 0, 7, 2], [2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
        },
		{
            "input": [[2, 2, 2, 2, 2, 2, 2], [2, 7, 7, 7, 7, 7, 2], [2, 7, 7, 7, 7, 7, 2], [2, 7, 7, 7, 7, 7, 2], [2, 7, 7, 7, 7, 7, 2], [2, 2, 2, 2, 2, 2, 2]],
            "output": [[2, 2, 2, 2, 2, 2, 2], [2, 7, 7, 7, 7, 7, 2], [2, 7, 0, 0, 0, 7, 2], [2, 7, 0, 0, 0, 7, 2], [2, 7, 7, 7, 7, 7, 2], [2, 2, 2, 2, 2, 2, 2]]
        }
    ]
}

results = calculate_metrics(task)
print(results)