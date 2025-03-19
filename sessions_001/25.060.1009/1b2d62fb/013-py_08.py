def report(grid, description):
    print(f"  {description}:")
    rows, cols = grid.shape
    print(f"    shape: {rows}x{cols}")
    unique_values = np.unique(grid)
    print(f"    unique values: {unique_values}")
    for value in unique_values:
        count = np.sum(grid == value)
        print(f"    count of {value}: {count}")

#example use - replace with actual grids from the problem
#report(input_grid, "Input Grid")

# Assuming 'transform' function and example_inputs, example_outputs are available

for i, (input_grid, output_grid) in enumerate(zip(example_inputs, example_outputs)):
    print(f"Example {i + 1}:")
    report(input_grid, "Input Grid")
    report(output_grid, "Expected Output Grid")
    predicted_output = transform(input_grid)
    report(predicted_output, "Predicted Output Grid")
    print("---")