import numpy as np

def get_nonzero_pixels(grid):
    nonzero_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_pixels.append((r, c, grid[r, c]))
    return nonzero_pixels

def transform(input_grid):
    nonzero_pixels = get_nonzero_pixels(input_grid)
    num_nonzero = len(nonzero_pixels)

    output_grid = np.zeros((num_nonzero, num_nonzero if num_nonzero > 1 else 1), dtype=int)

    if num_nonzero == 2:
        output_grid[0, 0] = nonzero_pixels[0][2]
        output_grid[1, 1] = nonzero_pixels[1][2]
        trimmed_output_grid = output_grid[:2, :2]
    elif num_nonzero == 1:
        output_grid[0,0] = nonzero_pixels[0][2]
        trimmed_output_grid = output_grid
    else:
        for i in range(num_nonzero):
            output_grid[i, 0] = nonzero_pixels[i][2]

        max_row = 0
        max_col = 0

        for r in range(output_grid.shape[0]):
          for c in range(output_grid.shape[1]):
            if output_grid[r,c] != 0:
              if r > max_row:
                max_row = r
              if c > max_col:
                max_col = c
        trimmed_output_grid = output_grid[:max_row+1,:max_col+1]

    print(f"Input:\n{input_grid}\nNon-zero pixels: {nonzero_pixels}")
    print(f"Output:\n{trimmed_output_grid}")
    return trimmed_output_grid

# Example usage with the training data (replace with actual data)
task_data = [
    {
        "input": np.array([[0, 0, 0], [0, 5, 0], [0, 0, 0]]),
        "output": np.array([[5]])
    },
    {
        "input": np.array([[0, 0, 0], [0, 5, 0], [0, 0, 9]]),
        "output": np.array([[5, 0], [0, 9]])
    },
    {
        "input": np.array([[0, 0, 7, 0, 0], [0, 5, 0, 0, 0], [0, 0, 9, 0, 0]]),
        "output": np.array([[7], [5], [9]])
    },
     {
        "input": np.array([[1, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [3, 0, 0, 4]]),
        "output": np.array([[1], [3], [2], [4]])
    }
]

for example in task_data:
    print(f"----- Example -----")
    transform(example["input"])
    print(f"Expected output:\n{example['output']}")
