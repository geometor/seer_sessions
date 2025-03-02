# Assume 'examples' is a list of (input_grid, expected_output_grid) tuples
# and transform is the current transform function

for i, (input_grid, expected_output_grid) in enumerate(examples):
    actual_output_grid = transform(input_grid)

    print(f"--- Example {i+1} ---")
    print("Input:")
    # pretty print the input_grid - use a library if available, otherwise print
    # as rows
    print(input_grid)

    print("\nExpected Output:")
    print(expected_output_grid)

    print("\nActual Output:")
    print(actual_output_grid)

    print("\nDifferences:")
    # Compare element-wise, and report discrepancies.
    input_arr = np.array(input_grid)
    expected_arr = np.array(expected_output_grid)
    actual_arr = np.array(actual_output_grid)

    if expected_arr.shape == actual_arr.shape: # only compare if shapes are compatible
        diff = expected_arr != actual_arr
        diff_indices = np.where(diff)
        for row, col in zip(*diff_indices):
            print(f"  Pixel at ({row}, {col}): Expected {expected_arr[row, col]}, Got {actual_arr[row, col]}")
    else:
        print("  Shapes of expected and actual outputs differ. Cannot do element-wise comparison.")
        print(f"expected shape: {expected_arr.shape}")
        print(f"actual shape: {actual_arr.shape}")
    print("\n")
