def analyze_transform(input_grid, output_grid, transform_func):
    transformed_grid = transform_func(input_grid)
    correct = transformed_grid == output_grid
    mismatches = []
    if not correct:

        for i in range(len(output_grid)):
            for j in range(len(output_grid[i])):
                if transformed_grid[i][j] != output_grid[i][j]:
                    mismatches.append({
                        'row': i,
                        'col': j,
                        'input_val': input_grid[i][j],
                        'expected_val': output_grid[i][j],
                        'transformed_val': transformed_grid[i][j]
                    })
    return correct, mismatches

# Example usage with the provided data:
task_data = [
    {
        "input": [[3, 1, 3, 3], [3, 3, 1, 2], [1, 3, 2, 3], [3, 2, 3, 1]],
        "output": [[4, 5, 4, 4], [4, 4, 5, 6], [5, 4, 6, 4], [4, 6, 4, 5]],
    },
    {
        "input": [[1, 3, 3, 2, 3], [3, 2, 1, 3, 3], [2, 3, 3, 3, 1]],
        "output": [[5, 4, 4, 6, 4], [4, 6, 5, 4, 4], [6, 4, 4, 4, 5]],
    },
    {
        "input": [[2, 2, 3, 3, 1, 3], [2, 3, 1, 3, 2, 3], [3, 3, 2, 3, 3, 2], [3, 1, 3, 3, 3, 3]],
        "output": [[6, 6, 4, 4, 5, 4], [6, 4, 5, 4, 6, 4], [4, 4, 6, 4, 4, 6], [4, 5, 4, 4, 4, 4]],
    },
]
def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = []
    for row in input_grid:
      output_grid.append(row.copy())

    # Iterate through each cell of the output grid.
    for i in range(len(output_grid)):
        for j in range(len(output_grid[i])):
            # Apply the value mapping.
            if output_grid[i][j] == 3:
                output_grid[i][j] = 4
            elif output_grid[i][j] == 1:
                output_grid[i][j] = 5
            elif output_grid[i][j] == 2:
                output_grid[i][j] = 6

    return output_grid

results = []
for example in task_data:
  results.append(analyze_transform(example["input"], example["output"], transform))
print(results)