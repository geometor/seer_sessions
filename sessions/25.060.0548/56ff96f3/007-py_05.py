def code_execution(input_grid, expected_output, result_grid, example_id):
    """
    Analyzes an example and the result, printing relevant metrics.
    """
    print(f"--- Example {example_id} ---")

    # Find non-white pixels in the input
    input_pixels = get_non_white_pixels(input_grid)
    print(f"Input Non-White Pixels: {input_pixels}")

    # Compare expected output and result
    diff = expected_output != result_grid
    diff_indices = np.where(diff)
    num_diffs = np.sum(diff)

    print(f"Number of Differences: {num_diffs}")
    if num_diffs > 0:
        print(f"Difference Indices (row, col): {list(zip(diff_indices[0], diff_indices[1]))}")

# Loop through examples and apply code_execution
for i, (input_grid, expected_output) in enumerate(train_pairs):
    result_grid = transform(np.array(input_grid))  # Ensure input is a NumPy array
    code_execution(np.array(input_grid), np.array(expected_output), result_grid, i + 1)
    print("\n")