import numpy as np

def get_2x2_block(grid):
    """Identifies the 2x2 block of non-zero pixels and returns their colors and positions."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            block = grid[r:r+2, c:c+2]
            if np.all(block != 0):
                return {
                    "top_left": (block[0, 0], (r, c)),
                    "top_right": (block[0, 1], (r, c + 1)),
                    "bottom_left": (block[1, 0], (r + 1, c)),
                    "bottom_right": (block[1, 1], (r + 1, c + 1)),
                }
    return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find 2 x 2 block
    block_2x2 = get_2x2_block(input_grid)
    if not block_2x2:
       return output_grid

    # Mirror top-left
    color_tl = block_2x2['bottom_right'][0]
    output_grid[0:2, 0:2] = color_tl

    # Mirror lower-right
    color_lr = block_2x2['top_left'][0]
    output_grid[rows-2:rows, cols-2:cols] = color_lr

    # Mirror top right
    color_tr = block_2x2['bottom_left'][0]
    output_grid[0:2, cols-2:cols] = color_tr

    # Mirror lower left
    color_ll = block_2x2['top_right'][0]
    output_grid[rows-2:rows, 0:2] = color_ll

    return output_grid.tolist()

train_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 2, 0], [0, 0, 0, 3, 4, 0], [0, 0, 0, 0, 0, 0]],
        "output": [[4, 4, 0, 0, 3, 3], [4, 4, 0, 0, 3, 3], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 2, 0], [0, 0, 0, 3, 4, 0], [2, 2, 0, 0, 1, 1], [2, 2, 0, 0, 1, 1]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 6, 0, 0, 0, 0], [0, 0, 7, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[8, 8, 0, 0, 0, 0, 7, 7], [8, 8, 0, 0, 0, 0, 7, 7], [0, 0, 5, 6, 0, 0, 0, 0], [0, 0, 7, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [6, 6, 0, 0, 0, 0, 5, 5], [6, 6, 0, 0, 0, 0, 5, 5]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 5, 0, 0, 0], [0, 0, 0, 0, 1, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[8, 8, 0, 0, 0, 0, 0, 1, 1], [8, 8, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 5, 0, 0, 0], [0, 0, 0, 0, 1, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 0, 0, 0, 0, 0, 3, 3], [5, 5, 0, 0, 0, 0, 0, 3, 3]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 8, 0, 0], [0, 0, 0, 7, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        "output": [[6, 6, 0, 0, 0, 7, 7], [6, 6, 0, 0, 0, 7, 7], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 8, 0, 0], [0, 0, 0, 7, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [8, 8, 0, 0, 0, 2, 2], [8, 8, 0, 0, 0, 2, 2]]
    }
]

results = []
for example in train_examples:
    input_grid = example['input']
    expected_output = example['output']
    actual_output = transform(input_grid)
    results.append(np.array_equal(expected_output, actual_output))

print(results)