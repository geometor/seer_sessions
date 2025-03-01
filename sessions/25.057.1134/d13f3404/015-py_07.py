import numpy as np

def describe_grid(grid):
    grid = np.array(grid)
    print(f"  Shape: {grid.shape}")
    print(f"  Unique values: {np.unique(grid)}")
    print(f"  First row: {grid[0, :]}")

def analyze_results(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        print(f"Example {i+1}:")
        input_grid = example['input']
        expected_output_grid = example['output']
        actual_output_grid = transform(input_grid)

        print("  Input:")
        describe_grid(input_grid)
        print("  Expected Output:")
        describe_grid(expected_output_grid)
        print("  Actual Output:")
        describe_grid(actual_output_grid)

        if np.array_equal(expected_output_grid, actual_output_grid):
            print("  Result: Pass")
        else:
            print("  Result: Fail")
            
task = {
    "name": "Example Task",
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5]]
        },
        {
            "input": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "output": [[1, 2, 3, 3, 2, 1], [4, 5, 6, 6, 5, 4], [7, 8, 9, 9, 8, 7], [7, 8, 9, 9, 8, 7], [4, 5, 6, 6, 5, 4], [1, 2, 3, 3, 2, 1]]
        },
        {
            "input": [[5, 5, 8, 5, 5], [5, 5, 8, 5, 5]],
            "output": [[5, 5, 8, 5, 5, 8, 5, 5], [5, 5, 8, 5, 5, 8, 5, 5]]
        }
    ]
}
analyze_results(task)