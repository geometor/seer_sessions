def describe_grid(grid):
    grid = np.array(grid)
    print(f"  Dimensions: {grid.shape}")
    #check for unique values
    print(f" Unique values: {np.unique(grid)}")

task_data = {
    "train": [
        {
            "input": [[5, 8, 5], [5, 5, 8], [8, 5, 5]],
            "output": [[5, 8, 5], [5, 5, 8], [8, 5, 5], [0, 8, 0], [0, 0, 8]],
        },
        {
            "input": [[6, 8, 6], [6, 6, 6]],
            "output": [[6, 8, 6], [6, 6, 6], [0, 8, 0]],
        },
        {
            "input": [[7, 7, 3, 7, 3], [7, 3, 7, 7, 7], [3, 3, 3, 7, 7], [3, 7, 3, 3, 7]],
            "output": [[7, 7, 3, 7, 3], [7, 3, 7, 7, 7], [3, 3, 3, 7, 7], [3, 7, 3, 3, 7], [0, 0, 7, 0, 0], [0, 0, 0, 7, 0]],
        },
        {
            "input": [[6, 1, 2, 6, 8], [6, 6, 6, 1, 1]],
            "output": [[6, 1, 2, 6, 8], [6, 6, 6, 1, 1], [0, 0, 0, 6, 0], [0, 0, 0, 0, 1]],
        },
    ],
    "test": [
    {
        "input": [[2, 2, 7, 2, 7], [2, 7, 7, 7, 2], [7, 7, 2, 7, 7], [7, 2, 7, 2, 7]],
        "output":[[2, 2, 7, 2, 7], [2, 7, 7, 7, 2], [7, 7, 2, 7, 7], [7, 2, 7, 2, 7], [0, 0, 7, 0, 0],[0, 0, 0, 0, 7]]
    }
    ]
}

for i, example in enumerate(task_data["train"]):
    print(f"Train Example {i+1}:")
    print("Input:")
    describe_grid(example["input"])
    print("Output:")
    describe_grid(example["output"])
    print("-" * 20)
for i, example in enumerate(task_data["test"]):
    print(f"Test Example {i+1}:")
    print("Input:")
    describe_grid(example["input"])
    print("Output:")
    describe_grid(example["output"])
    print("-" * 20)
