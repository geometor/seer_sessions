def describe_grid(grid, name):
    import numpy as np
    grid_array = np.array(grid)
    print(f"{name}:")
    print(f"  Shape: {grid_array.shape}")
    print(f"  Unique values: {np.unique(grid_array)}")

#provided examples are in a variable call 'task'
for i, example in enumerate(task["train"]):
    describe_grid(example["input"], f"Example {i+1} Input")
    describe_grid(example["output"], f"Example {i+1} Output")
