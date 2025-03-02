import numpy as np

def grid_diff(grid1, grid2):
    """Show differences between two grids"""
    if grid1.shape != grid2.shape:
        return "Different shapes"
    return grid1 - grid2

def analyze_examples(task):
    """Analyze training examples, calculate metrics, and compare outputs."""
    results = []
    for example in task["train"]:
        input_grid = np.array(example["input"])
        expected_output_grid = np.array(example["output"])
        predicted_output_grid = transform(input_grid)  # Assuming 'transform' is defined
        diff_grid = grid_diff(expected_output_grid,predicted_output_grid)

        example_data = {
            "input_shape": input_grid.shape,
            "output_shape": expected_output_grid.shape,
            "predicted_shape": predicted_output_grid.shape,
            "first_nonzero": get_first_nonzero(input_grid),
            "diff": diff_grid.tolist() if isinstance(diff_grid, np.ndarray) else diff_grid,
            "output_eq": np.array_equal(expected_output_grid, predicted_output_grid)
        }
        results.append(example_data)
    return results

# Example task data (replace with actual task data)
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0]],
            "output": [[1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 0]],
            "output": [[2, 0, 0, 0, 0], [2, 2, 0, 0, 0], [2, 2, 2, 0, 0], [2, 2, 2, 2, 0], [2, 2, 2, 2, 2]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 3, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "output": [[3, 0, 0, 0], [3, 3, 0, 0], [3, 3, 3, 0], [3, 3, 3, 3]],
        },
    ]
}

analysis_results = analyze_examples(task)
for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Input shape: {result['input_shape']}")
    print(f"  Output shape: {result['output_shape']}")
    print(f"  Predicted shape: {result['predicted_shape']}")
    print(f"  First nonzero: {result['first_nonzero']}")
    print(f"  Output Matches Expected: {result['output_eq']}")
    print(f"  Differences: {result['diff']}")