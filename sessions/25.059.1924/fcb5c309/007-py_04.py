import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # change output pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            # Fill border with yellow
            if (r == 0 or r == input_grid.shape[0] - 1 or
                c == 0 or c == input_grid.shape[1] - 1):
                output_grid[r, c] = 4
            elif input_grid[r,c] != 0:
                output_grid[r,c] = 4

    return output_grid.tolist()

def show_grid(grid, title="Grid"):
    grid = np.array(grid)
    print(title)
    print(grid)

examples = [
    {
        "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
        "output": [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]]
    },
    {
        "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
        "output": [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]]
    },
    {
        "input": [[6, 6, 6, 6, 6, 6, 6, 6], [6, 0, 0, 0, 0, 0, 0, 6], [6, 0, 0, 5, 5, 0, 0, 6], [6, 0, 0, 5, 5, 0, 0, 6], [6, 0, 0, 0, 0, 0, 0, 6], [6, 6, 6, 6, 6, 6, 6, 6]],
        "output": [[4, 4, 4, 4, 4, 4, 4, 4], [4, 0, 0, 0, 0, 0, 0, 4], [4, 0, 0, 5, 5, 0, 0, 4], [4, 0, 0, 5, 5, 0, 0, 4], [4, 0, 0, 0, 0, 0, 0, 4], [4, 4, 4, 4, 4, 4, 4, 4]]
    },
]

for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    generated_output = transform(input_grid)
    print(f"--- Example {i+1} ---")
    show_grid(input_grid, "Input")
    show_grid(expected_output, "Expected Output")
    show_grid(generated_output, "Generated Output")
    if generated_output == expected_output:
        print("Output: OKAY")
    else:
        print("Output: ERROR")