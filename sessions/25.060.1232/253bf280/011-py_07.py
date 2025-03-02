def analyze_example(example_number, input_grid, output_grid):
    """Analyzes a single example and provides metrics."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    azure_pixels_input = np.argwhere(input_grid == 8)
    green_pixels_output = np.argwhere(output_grid == 3)
    azure_pixels_output = np.argwhere(output_grid == 8)

    print(f"Example {example_number}:")
    print(f"  Azure pixels in input: {azure_pixels_input.tolist()}")
    print(f"  Azure pixels in output: {azure_pixels_output.tolist()}")
    print(f"  Green pixels in output: {green_pixels_output.tolist()}")

    # Check for green pixels adjacent to each azure pixel
    for row, col in azure_pixels_input:
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        green_neighbors = 0
        for n_row, n_col in neighbors:
            if 0 <= n_row < output_grid.shape[0] and 0 <= n_col < output_grid.shape[1] and output_grid[n_row, n_col] == 3:
                green_neighbors += 1
        print(f" Azure pixel at ({row}, {col}) has {green_neighbors} green neighbors in output.")

    #check for green blocks that are not adjacent to azure
    for row, col in green_pixels_output:
      neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
      azure_count = 0
      for r, c in neighbors:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          if output_grid[r,c] == 8:
            azure_count+=1
      print(f'Green pixel at ({row},{col}) is adjacent to {azure_count} azure pixels')
    print("-" * 20)


# Example usage (replace with actual input/output data from the task)
# Assume train_in, train_out lists exist from problem definition.
train_in = task["train_in"]
train_out = task["train_out"]

for i in range(len(train_in)):
    analyze_example(i + 1, train_in[i], train_out[i])
