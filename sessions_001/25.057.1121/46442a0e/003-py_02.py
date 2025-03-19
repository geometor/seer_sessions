import numpy as np

def get_grid_dimensions(grid):
    return grid.shape

def compare_grids(grid1, grid2):
    return np.array_equal(grid1, grid2)

def execute_transform(input_grid):
    output_grid = np.zeros((4, 4), dtype=int)
    for i in range(2):
        for j in range(2):
            output_grid[i*2][j*2] = input_grid[i][j]
            output_grid[i*2+1][j*2] = input_grid[i+1][j]
            output_grid[i*2][j*2+1] = input_grid[i][j+1]
            output_grid[i*2+1][j*2+1] = input_grid[i+1][j+1]

    return output_grid

#Example usage with Task Data (assuming it is stored similar to before)

task_data = {
    "train": [
        {
            "input": [[5, 5], [5, 8]],
            "output": [[5, 5, 5, 5], [5, 8, 5, 8], [5, 5, 5, 5], [5, 8, 5, 8]]
        },
        {
            "input": [[7, 0], [7, 7]],
            "output": [[7, 0, 7, 0], [7, 7, 7, 7], [7, 0, 7, 0], [7, 7, 7, 7]]
        },
        {
            "input": [[0, 7], [7, 7]],
            "output": [[0, 7, 0, 7], [7, 7, 7, 7], [0, 7, 0, 7], [7, 7, 7, 7]]
        },
        {
            "input": [[7, 0], [0, 0]],
              "output": [[7, 0, 7, 0], [0, 0, 0, 0], [7, 0, 7, 0], [0, 0, 0, 0]]
        }
    ],
    "test": [
        {
            "input": [[6, 6], [8, 0]],
            "output": [[6, 6, 6, 6], [8, 0, 8, 0], [6, 6, 6, 6], [8, 0, 8, 0]]
        }
    ]
}

results = {}
for i, example in enumerate(task_data["train"]):
    input_grid = np.array(example["input"])
    expected_output = np.array(example["output"])
    actual_output = execute_transform(input_grid)
    results[f"train_{i}"] = {
        "input_dimensions": get_grid_dimensions(input_grid),
        "output_dimensions": get_grid_dimensions(expected_output),
        "match": compare_grids(expected_output, actual_output)
    }

print(results)
