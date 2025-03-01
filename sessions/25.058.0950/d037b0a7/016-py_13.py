import numpy as np

example_data = [
    {
        "input": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 1, 0], [0, 1, 0]]),
    },
    {
        "input": np.array([[0, 0, 0], [0, 0, 2], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 0, 2], [0, 0, 2]]),
    },
    {
        "input": np.array([[0, 3, 0], [0, 0, 0], [0, 0, 0]]),
        "output": np.array([[0, 3, 0], [0, 3, 0], [0, 0, 0]]),
    },
    {
        "input": np.array([[4, 0, 0], [0, 0, 0], [0, 0, 0]]),
        "output": np.array([[4, 0, 0], [4, 0, 0], [0, 0, 0]]),
    }

]

for i, example in enumerate(example_data):
    input_grid = example["input"]
    output_grid = example["output"]
    print(f"Example {i+1}: Input Shape: {input_grid.shape}, Output Shape: {output_grid.shape}")
