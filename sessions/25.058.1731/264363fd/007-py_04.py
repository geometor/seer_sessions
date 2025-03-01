import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    description = f"Shape: {rows}x{cols}\n"
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    for color, count in color_counts.items():
        description += f"Color {color}: {count} pixels\n"
    return description

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        return "Shapes are different.\n"
    diff = grid1 != grid2
    diff_coords = np.where(diff)
    num_diffs = len(diff_coords[0])
    description = f"Number of differing pixels: {num_diffs}\n"
    if num_diffs > 0:
        description += "Differing pixel coordinates and values:\n"
        for i in range(num_diffs):
            r, c = diff_coords[0][i], diff_coords[1][i]
            description += f"  ({r}, {c}): Expected {grid2[r, c]}, Got {grid1[r, c]}\n"
    return description
train_ex = [
    ([
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 3, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    ],
     [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 2, 2, 2, 2, 2, 2, 2, 2, 8],
        [8, 2, 2, 2, 3, 2, 2, 2, 2, 8],
        [8, 2, 2, 2, 2, 2, 2, 2, 2, 8],
        [8, 2, 2, 2, 2, 2, 2, 2, 2, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    ]),
    ([
        [8, 8, 8, 8, 8, 8, 8, 8],
        [8, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 3, 3, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 0, 8],
        [8, 8, 8, 8, 8, 8, 8, 8],
    ],
     [
        [8, 8, 8, 8, 8, 8, 8, 8],
        [8, 2, 2, 2, 2, 2, 2, 8],
        [8, 2, 2, 3, 3, 2, 2, 8],
        [8, 2, 2, 2, 2, 2, 2, 8],
        [8, 2, 2, 2, 2, 2, 2, 8],
        [8, 8, 8, 8, 8, 8, 8, 8],
     ]),
    ([
        [8, 8, 8, 8, 8, 8, 8],
        [8, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 3, 0, 0, 8],
        [8, 0, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 3, 8],
        [8, 8, 8, 8, 8, 8, 8]
    ],
     [
        [8, 8, 8, 8, 8, 8, 8],
        [8, 2, 2, 2, 2, 2, 8],
        [8, 2, 2, 3, 2, 2, 8],
        [8, 2, 2, 2, 2, 2, 8],
        [8, 2, 2, 2, 2, 3, 8],
        [8, 8, 8, 8, 8, 8, 8],
     ]),
    ([
        [8, 8, 8, 8, 8, 8],
        [8, 3, 0, 0, 0, 8],
        [8, 0, 0, 0, 0, 8],
        [8, 0, 0, 0, 3, 8],
        [8, 8, 8, 8, 8, 8]
    ],
     [
        [8, 8, 8, 8, 8, 8],
        [8, 3, 2, 2, 2, 8],
        [8, 2, 2, 2, 2, 8],
        [8, 2, 2, 2, 3, 8],
        [8, 8, 8, 8, 8, 8],
     ])
]

from previous_code import transform

for i, (input_grid, expected_output) in enumerate(train_ex):
    input_grid_np = np.array(input_grid)
    expected_output_np = np.array(expected_output)
    actual_output_np = transform(input_grid_np)

    print(f"Example {i+1}:")
    print("Input Grid:")
    print(describe_grid(input_grid_np))
    print("Expected Output:")
    print(describe_grid(expected_output_np))
    print("Actual Output:")
    print(describe_grid(actual_output_np))
    print("Comparison:")
    print(compare_grids(actual_output_np, expected_output_np))
    print("-" * 20)