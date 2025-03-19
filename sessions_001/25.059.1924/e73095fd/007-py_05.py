import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid highlighting the differences."""
    diff_grid = np.zeros_like(grid1)
    for i in range(grid1.shape[0]):
      for j in range(grid1.shape[1]):
        if grid1[i,j] != grid2[i,j]:
          diff_grid[i,j] = 9
        else:
          diff_grid[i,j] = grid1[i,j]

    return diff_grid

def summarize_results(input_grid, expected_output, actual_output):

    print("Input Grid:")
    print(input_grid)
    print("Expected Output:")
    print(expected_output)
    print("Actual Output:")
    print(actual_output)
    print("Difference highlight:")
    print(compare_grids(expected_output, actual_output))
    diffs = np.where(expected_output != actual_output)
    num_diffs = len(diffs[0]) if diffs else 0
    print(f"Number of differing pixels: {num_diffs}")

    print("\n")

# Example data from the prompt (replace with actual task data)
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 0],
                           [0, 5, 5, 5, 5, 0],
                           [0, 5, 5, 5, 5, 0],
                           [0, 5, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 5, 5, 5, 5, 0],
                            [0, 5, 4, 4, 5, 0],
                            [0, 5, 4, 4, 5, 0],
                            [0, 5, 5, 5, 5, 0],
                            [0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 5, 0],
                           [0, 5, 5, 5, 5, 5, 0],
                           [0, 5, 5, 5, 5, 5, 0],
                           [0, 5, 5, 5, 5, 5, 0],
                           [0, 5, 5, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 5, 5, 5, 5, 5, 0],
                            [0, 5, 4, 4, 4, 5, 0],
                            [0, 5, 4, 4, 4, 5, 0],
                            [0, 5, 4, 4, 4, 5, 0],
                            [0, 5, 5, 5, 5, 5, 0],
                            [0, 0, 0, 0, 0, 0, 0]]),
    },
    {
       "input": np.array([[0, 0, 0, 0, 0, 0],
                          [0, 5, 5, 5, 5, 0],
                          [0, 5, 5, 5, 5, 0],
                          [0, 5, 5, 5, 5, 0],
                          [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 0],
                           [0, 5, 4, 4, 5, 0],
                           [0, 5, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0]]),
    },
]

for example in examples:
    summarize_results(example["input"], example["output"], transform(example["input"]))
