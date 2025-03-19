import numpy as np

def describe_grid(grid):
    grid = np.array(grid)
    rows, cols = grid.shape
    colors = np.unique(grid)
    return f"Shape: {rows}x{cols}, Colors: {colors}"

task = {
    "train": [
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 1, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 1, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[0, 0], [3, 0], [0, 3], [0, 0]],
        },
        {
            "input": [[8, 8, 8, 1, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 1, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[3, 0], [0, 0], [0, 3], [0, 0]],
        },
		{
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 7, 0, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0], [0, 0], [0, 0]],
        },
    ],
    "test": [
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 1, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[0], [0], [3], [0]],
        }
    ],
}

for i, example in enumerate(task["train"]):
    input_grid = example['input']
    output_grid = example['output']
    input_desc = describe_grid(input_grid)
    output_desc = describe_grid(output_grid)
    print(f"Example {i+1}:")
    print(f"  Input: {input_desc}")
    print(f"  Output: {output_desc}")


    # Call the transform function (defined in the prompt)
    transformed_grid = transform(input_grid)
    transformed_desc = describe_grid(transformed_grid)

    print(f"  Transformed Output: {transformed_desc}")    
    print(f"  Correct: {np.array_equal(transformed_grid, output_grid)}")
    print("-" * 20)