import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)

    # flip the grid vertically
    output_grid = np.flipud(output_grid)

    return output_grid

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        return False
    return np.array_equal(grid1, grid2)

# Dummy task data for demonstration. Replace with actual loaded task data.
train_examples = [
    {
        "input": np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]]),
        "output": np.array([[3, 3, 3], [2, 2, 2], [1, 1, 1]])
    },
        {
        "input": np.array([[5, 5, 5,5], [6, 6, 6,6]]),
        "output": np.array([[6, 6, 6,6], [5, 5, 5,5]])
    },
    {
        "input": np.array([[7, 7], [8, 8],[9,9]]),
        "output": np.array([[9,9], [8, 8],[7, 7]])
    },
]

results = []
for i, example in enumerate(train_examples):
    transformed_grid = transform(example["input"])
    is_correct = compare_grids(transformed_grid, example["output"])
    results.append(
        {
            "example_index": i,
            "input_shape": example["input"].shape,
            "output_shape": example["output"].shape,
            "transformed_shape": transformed_grid.shape,
            "is_correct": is_correct,
        }
    )

print(results)
