import numpy as np

train_examples = [
    {
        "input": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0], [0, 0, 5, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 8, 0, 0, 0], [0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]),
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 9, 0, 0],[0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]]),
    },
]

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    output_grid = example["output"]

    input_shape = input_grid.shape
    output_shape = output_grid.shape
    input_nonzero_count = np.count_nonzero(input_grid)
    output_nonzero_count = np.count_nonzero(output_grid)
    input_nonzero_values = input_grid[input_grid != 0]
    output_nonzero_values = output_grid[output_grid != 0]

    print(f"Example {i+1}:")
    print(f"  Input Shape: {input_shape}")
    print(f"  Output Shape: {output_shape}")
    print(f"  Input Non-zero Count: {input_nonzero_count}")
    print(f"  Output Non-zero Count: {output_nonzero_count}")
    print(f"  Input Non-zero Values: {input_nonzero_values}")
    print(f"  Output Non-zero Values: {output_nonzero_values}")
    print("-" * 20)