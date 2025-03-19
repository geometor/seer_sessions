import numpy as np

def get_grid_info(grid):
    """Returns dimensions and unique color counts of a grid."""
    return grid.shape, np.unique(grid, return_counts=True)

train_examples = [
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 6, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5]])
    },
     {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 6, 6, 6, 5, 5, 5, 5],
                           [5, 5, 5, 6, 6, 6, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
    },
        {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
    }

]

results = []
for i, example in enumerate(train_examples):
    input_info = get_grid_info(example["input"])
    output_info = get_grid_info(example["output"])
    results.append({
        "example": i + 1,
        "input_shape": input_info[0],
        "input_colors": dict(zip(input_info[1][0], input_info[1][1])),
        "output_shape": output_info[0],
        "output_colors": dict(zip(output_info[1][0], output_info[1][1])),
    })

for result in results:
    print(result)