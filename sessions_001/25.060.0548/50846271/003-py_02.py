import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a pixel-by-pixel difference."""
    grid1 = np.array(grid1)
    grid2 = np.array(grid2)

    if grid1.shape != grid2.shape:
        return "Failure: Different Dimensions"

    diff = grid1 != grid2
    if np.any(diff):
        return "Failure"
    else:
        return "Success"

def test_transform(transform_func, task):
    """Tests the transform function against all training examples."""
    results = []
    for example in task['train']:
        input_grid = example['input']
        expected_output_grid = example['output']
        actual_output_grid = transform_func(input_grid)
        comparison_result = compare_grids(expected_output_grid, actual_output_grid)
        results.append(comparison_result)
    return results
# Example usage with dummy task data:
task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0], [0, 2, 0, 2, 0], [0, 0, 2, 0, 0], [0, 2, 0, 2, 0], [0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0], [0, 8, 0, 8, 0], [0, 0, 8, 0, 0], [0, 8, 0, 8, 0], [0, 0, 0, 0, 0]],
        },
        {
            "input": [[2, 0, 0, 0, 2], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 2]],
            "output": [[8, 0, 0, 0, 8], [0, 0, 0, 0, 0], [0, 0, 8, 0, 0], [0, 0, 0, 0, 0], [8, 0, 0, 0, 8]],
        },
        {
           "input": [[2,2,2],[2,0,2],[2,2,2]],
           "output" : [[8,2,8],[8,0,8],[8,2,8]]
        }

    ]
}
results = test_transform(transform, task_data)
print(results)
