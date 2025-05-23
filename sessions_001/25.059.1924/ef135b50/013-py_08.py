import numpy as np

# Helper function to find differences between arrays
def find_differences(array1, array2):
    if array1.shape != array2.shape:
        return "Shapes are different"
    else:
        return np.where(array1 != array2)

train = [
    {
        "input":  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
                   [0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
                   [0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
                   [0, 0, 0, 2, 9, 9, 2, 0, 0, 0],
                   [0, 0, 0, 2, 9, 9, 2, 0, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input":  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
                   [0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
                   [0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
                   [0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
                   [0, 0, 0, 2, 2, 0, 2, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
                   [0, 0, 0, 2, 9, 9, 2, 0, 0, 0],
                   [0, 0, 0, 2, 9, 9, 2, 0, 0, 0],
                   [0, 0, 0, 2, 9, 9, 2, 0, 0, 0],
                   [0, 0, 0, 2, 2, 9, 2, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
        {
        "input":  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
                   [0, 0, 0, 2, 0, 0, 0, 2, 0, 0],
                   [0, 0, 0, 2, 0, 0, 0, 2, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
                   [0, 0, 0, 2, 9, 9, 9, 2, 0, 0],
                   [0, 0, 0, 2, 9, 9, 9, 2, 0, 0],
                   [0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    }
]

for i, example in enumerate(train):
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    predicted_grid = transform(input_grid)
    diff = find_differences(output_grid, predicted_grid)
    print(f"Example {i+1}:")
    print(f"  Differences (row, col): {diff}")
