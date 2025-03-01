def report(grid):
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Unique Colors: {unique_colors}")
    print(f"  Color Counts: {color_counts}")

for i, (input_grid, output_grid) in enumerate(zip(task.train_input_grids, task.train_output_grids)):
    print(f"Example {i+1}:")
    print("Input:")
    report(input_grid)
    print("Expected Output:")
    report(output_grid)
    predicted = transform(input_grid)
    print("Predicted Output")
    report(predicted)

    if np.array_equal(predicted,output_grid):
        print("Prediction: Correct")
    else:
        print("Prediction: Incorrect")