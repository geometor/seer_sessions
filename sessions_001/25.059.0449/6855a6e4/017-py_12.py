import numpy as np

def analyze_example(input_grid, output_grid, predicted_output_grid):
    """Analyzes a single example and provides metrics."""

    red_input_count = np.sum(input_grid == 2)
    gray_input_count = np.sum(input_grid == 5)
    red_output_count = np.sum(output_grid == 2)
    gray_output_count = np.sum(output_grid == 5)
    red_predicted_count = np.sum(predicted_output_grid == 2)
    gray_predicted_count = np.sum(predicted_output_grid == 5)

    metrics = {
        "red_input": int(red_input_count),
        "gray_input": int(gray_input_count),
        "red_output": int(red_output_count),
        "gray_output": int(gray_output_count),
        "red_predicted": int(red_predicted_count),
        "gray_predicted": int(gray_predicted_count),
        "gray_diff": int(gray_output_count - gray_predicted_count),
        "success": bool(np.array_equal(output_grid, predicted_output_grid))
    }
    return metrics

def get_in_out_grids(task, train_or_test, example_num):

    in_grid = np.array(task[train_or_test][example_num]['input'])
    out_grid = np.array(task[train_or_test][example_num]['output'])
    return in_grid, out_grid

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 2, 5, 2, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 2, 5, 2, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 5, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 5, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 0, 0, 2, 2], [0, 2, 5, 2, 0, 0, 2, 5], [0, 2, 2, 2, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 0, 0, 2, 2], [0, 2, 5, 2, 0, 0, 2, 5], [0, 2, 2, 2, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        }
    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        }
    ]
}

results = []
for i in range(len(task["train"])):
    in_grid, out_grid = get_in_out_grids(task, "train", i)
    predicted_output_grid = transform(in_grid)
    metrics = analyze_example(in_grid, out_grid, predicted_output_grid)
    metrics['example_num'] = i
    results.append(metrics)

print(results)
