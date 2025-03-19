def get_grid_info(grid):
    """Returns dimensions and unique values of a grid."""
    arr = np.array(grid)
    dimensions = arr.shape
    unique_values = np.unique(arr).tolist()
    return dimensions, unique_values

for i, example in enumerate(task["train"]):
    input_grid = example["input"]
    output_grid = example["output"]

    input_dims, input_values = get_grid_info(input_grid)
    output_dims, output_values = get_grid_info(output_grid)
    print(f"Example {i+1}:")
    print(f"  Input: Dimensions={input_dims}, Unique Colors={input_values}")
    print(f"  Output: Dimensions={output_dims}, Unique Colors={output_values}")
    print(f"  Correct? {np.array_equal(np.array(transform(input_grid)), np.array(output_grid))}")
