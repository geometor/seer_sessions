import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_non_blue_non_white = []
    input_rows, input_cols = input_grid.shape
    for r in range(input_rows):
        for c in range(input_cols):
            if input_grid[r, c] != 1 and input_grid[r,c] != 0:
                input_non_blue_non_white.append((r, c, input_grid[r,c]))

    output_non_blue_non_white = []
    output_rows, output_cols = output_grid.shape
    for r in range(output_rows):
        for c in range(output_cols):
            if output_grid[r, c] != 1 and output_grid[r,c] != 0:
              output_non_blue_non_white.append((r, c, output_grid[r,c]))

    print(f"  Input grid size: {input_grid.shape}")
    print(f"  Output grid size: {output_grid.shape}")
    print(f"  Input Non-blue/white pixels: {input_non_blue_non_white}")
    print(f"  Output Non-blue/white pixels: {output_non_blue_non_white}")
    print("-" * 20)
    return input_non_blue_non_white, output_non_blue_non_white

examples = [
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 3, 2, 1, 0, 0, 0], [0, 0, 0, 1, 2, 3, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[3, 2], [2, 3]]
    ),
     (
        [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 7, 7, 7, 7, 0, 0, 1], [1, 0, 0, 7, 2, 7, 8, 0, 0, 1], [1, 0, 0, 7, 7, 7, 7, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
        [[7, 7, 7, 7], [7, 2, 7, 8], [7, 7, 7, 7]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 5, 5, 5, 0, 1, 0], [0, 1, 0, 5, 4, 5, 0, 1, 0], [0, 1, 0, 5, 5, 5, 0, 1, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[5, 5, 5], [5, 4, 5], [5, 5, 5]]
    )

]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i + 1}:")
    analyze_example(input_grid, output_grid)