def compare_grids(grid1, grid2):
    """Counts the number of differing pixels between two grids."""
    return np.sum(grid1 != grid2)

def grid_to_string(grid):
    """Converts a NumPy grid to a string representation."""
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

# Load the task data (assuming it's loaded in a variable called 'task')
results = []
for i, example in enumerate(task['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    #predicted_output = transform(input_grid)  # Using the provided transform function - removed

    #diff_count = compare_grids(output_grid, predicted_output) #removed
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    #print(f"Example {i+1}:")
    #print(f"  Input shape: {input_shape}, Output shape: {output_shape}")
    #print(f"  Differences between predicted and actual output: {diff_count}")

    changed_pixels = compare_grids(input_grid, output_grid)
    #print(f"  Changes between input and output:{changed_pixels}")
    #print("Input Grid:")
    #print(grid_to_string(input_grid))
    #print("Output Grid:")
    #print(grid_to_string(output_grid))
    results.append({
      "example": i+1,
      "input_shape": input_shape,
      "output_shape": output_shape,
      "input_grid": grid_to_string(input_grid),
      "output_grid": grid_to_string(output_grid),
      "changed_pixels": changed_pixels,
      #"diff_count": diff_count #removed
    })
print(results)
