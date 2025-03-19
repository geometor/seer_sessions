def report(grid, name):
    print(f"--- {name} ---")
    print(grid)
    print(f"  shape: {grid.shape}")
    # colors and counts
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"  colors: {color_counts}")

# Example Usage
for i, (input_grid, output_grid) in enumerate(task.train):

    # show original input and output
    report(input_grid, f"input_{i}")
    report(output_grid, f"output_{i}")

    # apply the function
    transformed_grid = transform(input_grid)
    report(transformed_grid, f"transformed_{i}")
    if not np.array_equal(transformed_grid, output_grid):
      print("  Error: mismatch")