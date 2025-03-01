import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:
                if i <= 2 and j <= 2:
                    output_grid[i,j] = 1
                elif (i >= rows -3  or i <=2) and j>= cols -3:
                    output_grid[i, j] = 2
                elif i >= 4 and i <= rows-4 and j>= cols -3:
                     output_grid[i, j] = 2
                elif (i == 0 or i == rows -1) and ( j<=2 or j>= cols -3):
                    output_grid[i, j] = 3
                elif (i == 0 or i == rows -1):
                    output_grid[i,j] = 3
                elif (j == 0 and i <=2) or (j == cols-1 and i ==rows -2):
                    output_grid[i, j] = 3
                elif i >= 4 and i<= rows -4 and (j<=2):
                    output_grid[i, j] = 3


    return output_grid

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        return "Different shapes"
    else:
        return np.where(grid1 != grid2)

# Training examples -  manually copied to keep this executable
train_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1, 1, 1, 3, 3, 3, 3, 2, 2, 2],
                           [1, 1, 1, 3, 3, 3, 3, 2, 2, 2],
                           [1, 1, 1, 3, 3, 3, 3, 2, 2, 2],
                           [3, 3, 3, 5, 5, 5, 5, 2, 2, 2],
                           [3, 3, 3, 5, 5, 5, 5, 2, 2, 2],
                           [3, 3, 3, 5, 5, 5, 5, 2, 2, 2],
                           [3, 3, 3, 5, 5, 5, 5, 2, 2, 2],
                           [3, 3, 3, 3, 3, 3, 3, 2, 2, 2],
                           [3, 3, 3, 3, 3, 3, 3, 2, 2, 2],
                           [3, 3, 3, 3, 3, 3, 3, 2, 2, 2]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1, 1, 1, 3, 3, 3, 2, 2, 2],
                           [1, 1, 1, 3, 3, 3, 2, 2, 2],
                           [1, 1, 1, 3, 3, 3, 2, 2, 2],
                           [3, 3, 3, 5, 5, 5, 2, 2, 2],
                           [3, 3, 3, 5, 5, 5, 2, 2, 2],
                           [3, 3, 3, 5, 5, 5, 2, 2, 2],
                           [3, 3, 3, 3, 3, 3, 2, 2, 2],
                           [3, 3, 3, 3, 3, 3, 2, 2, 2],
                           [3, 3, 3, 3, 3, 3, 2, 2, 2]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 5, 5, 0, 0],
                           [0, 0, 0, 5, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1, 1, 1, 3, 2, 2, 2],
                           [1, 1, 1, 3, 2, 2, 2],
                           [1, 1, 1, 5, 5, 2, 2],
                           [1, 1, 1, 5, 5, 2, 2],
                           [1, 1, 1, 3, 2, 2, 2],
                           [1, 1, 1, 3, 2, 2, 2]]),
    },
]

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(input_grid)
    diff = compare_grids(expected_output, actual_output)
    print(f"Example {i+1}:")
    if isinstance(diff, str):
        print(f"  {diff}")
    else:
        if diff[0].size == 0:
            print("  No differences found.")
        else:
            print(f"  Differences at indices: {diff}")
            for row, col in zip(diff[0], diff[1]):
                print(f" location: ({row},{col}) expected: {expected_output[row,col]}  actual: {actual_output[row,col]}")