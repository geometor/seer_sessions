def get_target_indices(input_grid):
    """Finds rows and columns containing non-zero values."""
    rows = []
    cols = []
    for i, row in enumerate(input_grid):
        if any(val != 0 for val in row):
            rows.append(i)
    for j in range(input_grid.shape[1]):
        if any(input_grid[i][j] != 0 for i in range(input_grid.shape[0])):
            cols.append(j)
    return rows, cols

# I need to recreate the task examples, including this new one, in order
# to produce the report requested

train_examples = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [[3, 0], [0, 0]],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [[7, 0], [0, 4]],
    },
    {
           "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 9, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [[9]]
    }
]

# Iterate through each example pair
for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]

    # Call the existing transform function to see its output
    target_rows, target_cols = get_target_indices(input_grid)
    print(f"Example {i+1}:")
    print(f"  Target Rows: {target_rows}")
    print(f"  Target Columns: {target_cols}")

