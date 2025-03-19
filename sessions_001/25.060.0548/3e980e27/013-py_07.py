import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    rows_in, cols_in = input_grid.shape
    rows_out, cols_out = output_grid.shape
    diff = output_grid - input_grid
    print(f"Input shape: {input_grid.shape}")
    print(f"Output shape: {output_grid.shape}")
    # find changes
    if not np.array_equal(input_grid, output_grid):
        row_diffs = np.where(np.any(diff != 0, axis=1))[0]
        col_diffs = np.where(np.any(diff != 0, axis=0))[0]

        print(f"Rows with differences: {row_diffs}")
        print(f"Cols with differences: {col_diffs}")
        for r in row_diffs:
            print(f"Row {r}: Input {input_grid[r,:]} vs. Output {output_grid[r,:]}")
        for c in col_diffs:
            print(f"Col {c}: Input {input_grid[:,c]} vs. Output {output_grid[:,c]}")

    else:
        print("Input and output are identical.")

    for r in range(rows_in - 2):
        for c in range(cols_in - 2):
            block = input_grid[r:r+3, c:c+3]
            if np.all(block) and block[0,0] != 0:
                print(f"3x3 block found at ({r}, {c}) with color {block[0,0]}")

# Example Data (replace with actual data from the task)
example_pairs = [
    (
        [[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8]],
        [[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8]]
    ),
     (
        [[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]],
        [[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]]
    ),
    (
        [[2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2]]
    ),
    (
        [[8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8]],
        [[8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8]]
    ),
       (
        [[3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3]],
        [[3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3]]
    ),
]


for i, (input_grid, output_grid) in enumerate(example_pairs):
    print(f"---- Example {i+1} ----")
    analyze_example(input_grid, output_grid)