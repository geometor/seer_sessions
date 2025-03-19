import numpy as np

# Provided code (transform, find_contiguous_regions, is_fully_enclosed, get_inner_pixels) goes here.
# Assuming it's already defined above.
def show(grid):
    display(grid)

def compare(grid_a, grid_b):
    print(np.array_equal(grid_a, grid_b))

def analyze_results(task):
    print(f"Task: {task['id']}")
    results = []

    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        actual_output = transform(input_grid)
        is_correct = np.array_equal(actual_output, expected_output)
        results.append({
            'input': input_grid,
            'expected_output': expected_output,
            'actual_output': actual_output,
            'is_correct': is_correct
        })
        print(f"  Example: is_correct={is_correct}")
        show(input_grid)
        show(expected_output)
        show(actual_output)

    return results

# example usage (assuming 'task' variable with train/test structure exists)
task = {
    "id": "Example Task",
    "train": [
         {
            "input": [[0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 0], [0, 5, 1, 1, 5, 0], [0, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 0], [0, 5, 2, 2, 5, 0], [0, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 0], [0, 5, 1, 1, 1, 5, 0], [0, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 0], [0, 5, 2, 2, 2, 5, 0], [0, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[5, 5, 5, 5, 5], [5, 1, 1, 1, 5], [5, 1, 5, 1, 5], [5, 1, 1, 1, 5], [5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5], [5, 2, 2, 2, 5], [5, 2, 5, 2, 5], [5, 2, 2, 2, 5], [5, 5, 5, 5, 5]],
        },
		{
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5],
                      [5, 0, 0, 0, 0, 0, 0, 0, 5],
                      [5, 0, 5, 5, 5, 5, 5, 0, 5],
                      [5, 0, 5, 0, 0, 0, 5, 0, 5],
                      [5, 0, 5, 0, 0, 0, 5, 0, 5],
                      [5, 0, 5, 0, 0, 0, 5, 0, 5],
                      [5, 0, 5, 5, 5, 5, 5, 0, 5],
                      [5, 0, 0, 0, 0, 0, 0, 0, 5],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5],
                       [5, 0, 0, 0, 0, 0, 0, 0, 5],
                       [5, 0, 5, 5, 5, 5, 5, 0, 5],
                       [5, 0, 5, 2, 2, 2, 5, 0, 5],
                       [5, 0, 5, 2, 2, 2, 5, 0, 5],
                       [5, 0, 5, 2, 2, 2, 5, 0, 5],
                       [5, 0, 5, 5, 5, 5, 5, 0, 5],
                       [5, 0, 0, 0, 0, 0, 0, 0, 5],
                       [5, 5, 5, 5, 5, 5, 5, 5, 5]]
        },
        {
            "input":  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                       [0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                       [0, 5, 0, 5, 5, 5, 5, 5, 0, 5, 0],
                       [0, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0],
                       [0, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0],
                       [0, 5, 0, 5, 5, 5, 5, 5, 0, 5, 0],
                       [0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                       [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                       [0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                       [0, 5, 0, 5, 5, 5, 5, 5, 0, 5, 0],
                       [0, 5, 0, 5, 2, 2, 2, 5, 0, 5, 0],
                       [0, 5, 0, 5, 2, 2, 2, 5, 0, 5, 0],
                       [0, 5, 0, 5, 5, 5, 5, 5, 0, 5, 0],
                       [0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                       [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        }

    ]
}
analysis_results = analyze_results(task)
