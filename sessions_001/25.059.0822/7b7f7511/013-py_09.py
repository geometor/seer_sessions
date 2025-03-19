import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    print("Input Grid:")
    print(input_grid)
    print("Output Grid:")
    print(output_grid)

    rows, cols = input_grid.shape
    new_cols = cols // 2

    for j in range(new_cols):
        col1 = input_grid[:, 2*j]
        col2 = input_grid[:, 2*j + 1]
        out_col = output_grid[:, j]

        print(f"Comparing Input Columns {2*j} and {2*j+1} to Output Column {j}:")

        for i in range(rows):
          print(f"Row {i}: Input ({col1[i]}, {col2[i]}), Output: {out_col[i]}")

examples = [
    (
        [[8, 8, 8, 8, 8, 8]],
        [[8, 8, 8]]
    ),
     (
        [[8, 7, 8, 7, 8, 7],
         [8, 7, 8, 7, 8, 7]],
        [[8, 8, 8],
         [8, 8, 8]]
    ),
    (
        [[0, 1, 2, 3, 4, 5],
         [6, 7, 8, 9, 0, 1],
         [2, 3, 4, 5, 6, 7]],
        [[1, 3, 5],
         [7, 9, 1],
         [3, 5, 7]]
    ),
    (
        [[7, 2, 7, 2, 7, 2],
         [7, 2, 7, 2, 7, 2],
         [7, 2, 7, 2, 7, 2]],
        [[7, 7, 7],
         [7, 7, 7],
         [7, 7, 7]]
    ),
    (
       [[0, 0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2, 2]],
       [[0, 1, 2],
        [0, 1, 2],
        [0, 1, 2],
        [0, 1, 2]]
    )
]

for input_grid, output_grid in examples:
    analyze_example(input_grid, output_grid)
    print("-" * 20)