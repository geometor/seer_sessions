# Expected output grid (from the ARC task definition)
expected_output_2 = np.array([[0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]])

# Get the actual output from the provided code (already executed)
actual_output_2 = transform(input_grids[1].copy(), 2)

# Compare
comparison_2 = expected_output_2 == actual_output_2
print(comparison_2)
print(f"Number of differences: {np.sum(comparison_2 == False)}")
