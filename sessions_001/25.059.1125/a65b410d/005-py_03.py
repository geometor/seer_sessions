import numpy as np

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        return "Different Shapes"
    else:
        return np.array_equal(grid1, grid2)

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]]),
        "output": np.array([[0, 3, 0], [0, 2, 0], [0, 0, 0]]),
        "predicted": np.array([[0, 3, 0], [0, 2, 0], [0, 1, 0]])
    },
     {
        "input": np.array([[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 0]]),
        "output": np.array([[0, 3, 3, 0], [0, 2, 2, 0], [0, 0, 0, 0]]),
        "predicted": np.array([[0, 3, 3, 0], [0, 2, 2, 0], [0, 1, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 3, 0, 0], [0, 0, 2, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0]]),
        "predicted": np.array([[0, 3, 3, 3, 0], [0, 0, 2, 0, 0], [0, 0, 2, 0, 0], [0, 1, 0, 0, 0]])
    },
    {
        "input": np.array([[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        "output": np.array([[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
         "predicted": np.array([[2, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
    }
]

results = []
for i, example in enumerate(examples):
    comparison = compare_grids(example["output"], example["predicted"])
    results.append(
        {
            "example": i + 1,
            "input_shape": example["input"].shape,
            "output_shape": example["output"].shape,
            "predicted_shape": example["predicted"].shape,
            "match": comparison,
        }
    )

print(results)
