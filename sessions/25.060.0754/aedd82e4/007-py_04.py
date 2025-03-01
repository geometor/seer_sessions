import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change the color of the bottom-left pixel from red(2) to blue(1)
    if output_grid[2, 0] == 2:
      output_grid[2, 0] = 1

    return output_grid

# Training examples (replace with actual data from the task)
train_examples = [
    {
        "input": np.array([[5, 5, 5], [5, 5, 5], [2, 5, 5]]),
        "output": np.array([[5, 5, 5], [5, 5, 5], [1, 5, 5]]),
    },
    {
        "input": np.array([[0, 0, 0], [0, 0, 0], [2, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 0, 0], [1, 0, 0]]),
    },
    {
        "input": np.array([[8, 8, 8], [8, 8, 8], [8, 8, 8]]),
        "output": np.array([[8, 8, 8], [8, 8, 8], [8, 8, 8]]),
    },
    {
        "input": np.array([[4, 4, 4], [4, 4, 4], [2, 4, 4]]),
        "output": np.array([[4, 4, 4], [4, 4, 4], [1, 4, 4]]),
    },
]

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    comparison = np.array_equal(predicted_output, expected_output)
    print(f"Example {i + 1}:")
    print(f"  Input:\n{input_grid}")
    print(f"  Expected Output:\n{expected_output}")
    print(f"  Predicted Output:\n{predicted_output}")
    print(f"  Match: {comparison}")
    print("-" * 20)