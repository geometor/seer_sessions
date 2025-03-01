def compare_grids(grid1, grid2):
    """Counts the number of differing pixels between two grids."""
    return np.sum(grid1 != grid2)

# Load the task data (assuming it's loaded in a variable called 'task')

for i, example in enumerate(task['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = transform(input_grid)  # Using the provided transform function

    diff_count = compare_grids(output_grid, predicted_output)
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    print(f"Example {i+1}:")
    print(f"  Input shape: {input_shape}, Output shape: {output_shape}")
    print(f"  Differences between predicted and actual output: {diff_count}")

    changed_pixels = compare_grids(input_grid, output_grid)
    print(f"  Changes between input and output:{changed_pixels}")