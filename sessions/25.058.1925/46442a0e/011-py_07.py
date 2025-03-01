import numpy as np

def compare_grids(grid1, grid2):
    """
    Compares two grids element-wise and returns a grid of differences.
    0 indicates a match, 1 indicates a mismatch.
    """
    array1 = np.array(grid1)
    array2 = np.array(grid2)
    if array1.shape != array2.shape:
        return "Dimensions do not match"
    else:
         return (array1 != array2).astype(int)

# Example usage (replace with actual and expected outputs)
# diff_grid = compare_grids(actual_output, expected_output)
# print(diff_grid)

def array_to_string(arr):
    return np.array2string(np.array(arr))
# Example usage:
tasks = [
    {
        "input": [[5, 5, 5], [5, 8, 5], [5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 8, 8, 5, 5], [5, 5, 8, 8, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5]]
    },
    {
        "input": [[6, 6, 8], [6, 6, 8]],
        "output": [[6, 6, 6, 6, 8, 8], [6, 6, 6, 6, 8, 8], [6, 6, 6, 6, 8, 8], [6, 6, 6, 6, 8, 8]]
    },
    {
        "input" : [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        "output": [[1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1]]
    },
     {
        "input": [[9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9]],
        "output": [[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]]
    },
    {
        "input": [[7, 0, 7, 0], [0, 7, 0, 7], [7, 0, 7, 0], [0, 7, 0, 7]],
        "output": [[7, 7, 0, 0, 7, 7, 0, 0], [7, 7, 0, 0, 7, 7, 0, 0], [0, 0, 7, 7, 0, 0, 7, 7], [0, 0, 7, 7, 0, 0, 7, 7], [7, 7, 0, 0, 7, 7, 0, 0], [7, 7, 0, 0, 7, 7, 0, 0], [0, 0, 7, 7, 0, 0, 7, 7], [0, 0, 7, 7, 0, 0, 7, 7]]
    }

]

for i, task in enumerate(tasks):
    input_grid = task['input']
    expected_output = task['output']
    actual_output = transform(input_grid)
    diff_grid = compare_grids(actual_output, expected_output)
    print(f"Example {i+1}:")
    print(f"Input:\n{array_to_string(input_grid)}")
    print(f"Expected Output:\n{array_to_string(expected_output)}")
    print(f"Actual Output:\n{array_to_string(actual_output)}")
    print(f"Difference:\n{diff_grid}\n")