import numpy as np

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 0, 0], [0, 0, 8, 3, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[1, 2, 1, 2, 1, 2], [8, 3, 8, 3, 8, 3], [1, 2, 1, 2, 1, 2], [8, 3, 8, 3, 8, 3], [1, 2, 1, 2, 1, 2], [8, 3, 8, 3, 8, 3]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 7, 0, 0, 0], [0, 0, 0, 7, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7]]
        },
    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0], [0, 0, 7, 0, 0], [0, 0, 7, 0, 0], [0, 0, 0, 0, 0]],
            "output": [[7, 7, 7, 7, 7], [7, 7, 7, 7, 7], [7, 7, 7, 7, 7], [7, 7, 7, 7, 7]]
        }
    ]
}

def get_nonzero_pixels(grid):
    grid = np.array(grid)
    rows, cols = np.where(grid != 0)
    return list(zip(rows, cols, grid[rows, cols]))

for i, example in enumerate(task['train']):
    input_pixels = get_nonzero_pixels(example['input'])
    output_pixels = get_nonzero_pixels(example['output'])
    print(f"Train Example {i+1}:")
    print(f"  Input Non-zero Pixels: {input_pixels}")
    print(f"  Output Non-zero Pixels: {output_pixels}")
    print("-" * 20)
for i, example in enumerate(task['test']):
    input_pixels = get_nonzero_pixels(example['input'])
    output_pixels = get_nonzero_pixels(example['output'])
    print(f"Test Example {i+1}:")
    print(f"  Input Non-zero Pixels: {input_pixels}")
    print(f"  Output Non-zero Pixels: {output_pixels}")
    print("-" * 20)