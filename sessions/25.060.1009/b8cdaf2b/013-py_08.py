import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    h, w = input_grid.shape
    mirrored = []
    zeros = []
    bottom_rows_same = True

    # Check bottom two rows
    if h >= 2:  # Make sure there are at least two rows
        if not np.array_equal(input_grid[-2:, :], output_grid[-2:, :]):
            bottom_rows_same = False

    # Check for mirroring and zero placement
    for r in range(h):
        for c in range(w):
            if input_grid[r, c] != 0 and output_grid[r, w - 1 - c] == input_grid[r, c] and input_grid[r,c] == output_grid[r,c] :
                mirrored.append(((r, c), input_grid[r, c]))
            if output_grid[r, c] == 0 and input_grid[r,c] != 0:
                zeros.append(((r, c), input_grid[r,c]))

    return {
        "bottom_rows_same": bottom_rows_same,
        "mirrored": mirrored,
        "zeros": zeros,
    }

# Example data (replace with actual data from the task)
examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5]],
        "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5]],
    },
      {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 5, 5]],
        "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 5, 5]],
    },
      {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 0, 0]],
    },
     {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 5, 5]],
        "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 5, 5]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 5, 5]],
        "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 5, 5]],
    },

]

results = [analyze_example(ex["input"], ex["output"]) for ex in examples]
print(results)
