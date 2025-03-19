import numpy as np

# Define the input and output grids for each example
train_examples = [
    {
        "input": np.array([
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
        ]),
        "output": np.array([
            [5, 5],
            [5, 5],
            [5, 5],
            [5, 5],
            [5, 5],
            [5, 5],
        ]),
    },
    {
        "input": np.array([
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
        ]),
        "output": np.array([
            [7, 7],
            [7, 7],
            [7, 7],
            [7, 7],
            [7, 7],
            [7, 7],
            [7, 7],
        ]),
    },
    {
        "input": np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]),
        "output": np.array([
            [1, 1],
            [1, 1],
            [1, 1],
        ]),
    },
    {
        "input": np.array([
            [8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8],
        ]),
        "output": np.array([
            [8, 8],
            [8, 8],
            [8, 8],
            [8, 8],
            [8, 8],
        ]),
    },
]

# Create a list to store the shapes
shapes = []

# Iterate through each example and get the shapes
for example in train_examples:
    input_shape = example["input"].shape
    output_shape = example["output"].shape
    shapes.append({"input": input_shape, "output": output_shape})

# Print the shapes
for i, shape in enumerate(shapes):
    print(f"Example {i+1}: Input Shape = {shape['input']}, Output Shape = {shape['output']}")