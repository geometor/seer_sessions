# Recreate the transform function (for completeness within this execution)
def transform(input_grid):
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 5:
                output_grid[i, j] = 3
            elif input_grid[i, j] == 0:
                output_grid[i, j] = 4
            else:
                output_grid[i,j] = input_grid[i,j]
    return output_grid

examples = [
    (np.array([[5, 1, 5], [1, 0, 1], [5, 1, 5]]), np.array([[3, 1, 3], [1, 4, 1], [3, 1, 3]])),
    (np.array([[0, 1, 0], [1, 5, 1], [0, 1, 0]]), np.array([[4, 1, 4], [1, 3, 1], [4, 1, 4]])),
    (np.array([[5, 0, 5], [0, 1, 0], [5, 0, 5]]), np.array([[3, 4, 3], [4, 1, 4], [3, 4, 3]])),
]

for i, (input_grid, expected_output) in enumerate(examples):
    actual_output = transform(input_grid)
    print(f"Example {i+1}:")
    print("Input:\n", input_grid)
    print("Expected Output:\n", expected_output)
    print("Actual Output:\n", actual_output)
    print(compare_grids(expected_output, actual_output))
    print("-" * 20)