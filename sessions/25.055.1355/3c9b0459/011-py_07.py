def describe_grid(grid, name):
    """Provides a concise description of a grid."""
    np_grid = np.array(grid)
    height, width = np_grid.shape
    unique_colors = np.unique(np_grid)
    print(f"{name}:")
    print(f"  Dimensions: {width}x{height}")
    print(f"  Unique Colors: {list(unique_colors)}") # convert to list

def compare_grids(grid1, grid2):
    """Compares two grids for equality."""
    np_grid1 = np.array(grid1)
    np_grid2 = np.array(grid2)
    if np_grid1.shape != np_grid2.shape:
        print("  Shapes are different.")
        return False
    else:
        print("  Shapes are the same.")
    if np.array_equal(np_grid1, np_grid2):
        print("  Grids are identical.")
        return True
    else:
        print("  Grids are different.")
        diff = np_grid1 != np_grid2
        num_diff = np.sum(diff)
        print(f"Number of different pixels = {num_diff}.")
        return False

examples = task["train"]
for i, example in enumerate(examples):
  print(f"Example {i + 1}:")
  input_grid = example["input"]
  output_grid = example["output"]
  describe_grid(input_grid, "  Input")
  describe_grid(output_grid, "  Output")
  compare_grids(input_grid, output_grid)
  transformed_grid = transform(input_grid)
  describe_grid(transformed_grid, " Transform")
  compare_grids(output_grid, transformed_grid)
  print("-" * 20)

