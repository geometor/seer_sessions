# Expected output grid (from the ARC task definition)
expected_output_1 = np.array([[0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2, 0, 2]])

# Get the actual output from the provided code (already executed)
actual_output_1 = transform(input_grids[0].copy(), 1)

# Compare
comparison_1 = expected_output_1 == actual_output_1
print(comparison_1)
print(f"Number of differences: {np.sum(comparison_1 == False)}")
