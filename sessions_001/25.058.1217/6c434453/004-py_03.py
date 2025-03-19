import numpy as np

def find_crosses(grid):
    """
    Identifies centers of 3x3 crosses (plus signs) of a specific color in the grid.
    """
    cross_centers = []
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if (grid[r, c] == 1 and
                grid[r-1, c] == 1 and
                grid[r+1, c] == 1 and
                grid[r, c-1] == 1 and
                grid[r, c+1] == 1):
                cross_centers.append((r, c))
    return cross_centers

task = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 0, 2, 0, 0],
                [0, 2, 2, 2, 2, 2, 0],
                [0, 0, 2, 0, 2, 0, 0],
                [0, 2, 2, 2, 2, 2, 0],
                [0, 0, 2, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 0, 2, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 2, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
        },
    ]
}

def cross_data(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        cross_centers = find_crosses(input_grid)
        results.append(
            {
                'input': example['input'],
                'output': example['output'],
                'cross_centers': cross_centers
            }
        )

    return results

results = cross_data(task)
for result in results:
    print(result)