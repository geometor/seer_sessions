import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    in_rows, in_cols = input_grid.shape
    out_rows, out_cols = output_grid.shape
    print(f"Input Dimensions: {in_rows}x{in_cols}")
    print(f"Output Dimensions: {out_rows}x{out_cols}")
    # Check for mirroring - simplified.
    print("Mirroring check (row-wise):")

    if (in_rows == out_rows):
        for r in range(in_rows):
            print(f"Row {r}: Input: {input_grid[r]}, Output: {output_grid[r]}")
            print(f"Flipped Row {r}: Input: {input_grid[r][::-1]}, Output: {output_grid[r]}")


# Example data from prompt
training_examples = [
    {
        "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        "output": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
    },
     {
        "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 8, 0], [0, 0, 0, 0]],
        "output": [[0, 0, 0, 0], [0, 0, 8, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    },
    {
        "input": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "output": [[3, 2, 1], [6, 5, 4], [9, 8, 7]],
    },
]

for i, example in enumerate(training_examples):
    print(f"\n--- Example {i+1} ---")
    analyze_example(example["input"], example["output"])
