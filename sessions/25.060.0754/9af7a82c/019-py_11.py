import numpy as np

# Example grids (replace with actual data from the task)
train_examples = [
    {
        "input": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
        "output": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
    },
     {
        "input": np.array([[5, 5, 5, 5], [5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5], [5, 5, 5, 5]]),
    },
    {
        "input": np.array([[8, 8], [8, 8], [8, 8], [8,8]]),
        "output": np.array([[8, 8], [8, 8], [8, 8], [8,8]]),
    },
    {
        "input": np.array([[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]]),
        "output": np.array([[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]]),
    },
       {
        "input": np.array([[4, 4, 4], [4, 4, 4], [4, 4, 4],[4,4,4]]),
        "output": np.array([[4, 4, 4], [4, 4, 4], [4, 4, 4],[4,4,4]]),
    },
]

results = []

for example in train_examples:
    input_grid = example["input"]
    output_grid = example["output"]
    # Execute the transform function
    transformed_grid = np.copy(input_grid)
    result = np.array_equal(transformed_grid, output_grid)

    results.append(
        {
            "input_shape": input_grid.shape,
            "output_shape": output_grid.shape,
            "transform_successful": result,
        }
    )

print(results)