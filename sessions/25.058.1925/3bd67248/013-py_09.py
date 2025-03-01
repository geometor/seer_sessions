import numpy as np

def calculate_metrics(input_grid, expected_output_grid, transform_output_grid):
    total_pixels = input_grid.size
    correct_pixels = np.sum(expected_output_grid == transform_output_grid)
    incorrect_pixels = total_pixels - correct_pixels
    accuracy = (correct_pixels / total_pixels) * 100 if total_pixels>0 else 0
    changed_pixels = np.sum(input_grid != expected_output_grid)
    return {
        "input_shape": input_grid.shape,
        "output_shape": expected_output_grid.shape,
        "pixels_changed": changed_pixels,
        "correct_pixels": correct_pixels,
        "incorrect_pixels": incorrect_pixels,
        "accuracy": accuracy,
    }

def compare_outputs(task):
    metrics_list = []
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        transform_output_grid = transform(input_grid)
        metrics = calculate_metrics(input_grid, expected_output_grid, transform_output_grid)
        metrics_list.append( {
            "example": i,
            **metrics
            })

    for m in metrics_list:
        print(m)

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0]],
            "output": [[0, 2, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0], [0, 4, 0, 5, 0, 0], [0, 0, 0, 0, 4, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 5, 0, 0], [0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 5, 0, 0], [0, 5, 0, 0, 2, 0, 0], [0, 4, 0, 0, 0, 0, 0]],
        },
    ]
}

compare_outputs(task)