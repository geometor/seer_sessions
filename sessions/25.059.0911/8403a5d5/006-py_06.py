# Expected output grid (from the ARC task definition)
expected_output_3 = np.array([[0, 0, 0, 0, 2, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0],
       [0, 0, 0, 0, 5, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0]])

# Get the actual output from the provided code
actual_output_3 = transform(input_grids[2].copy(), 3)

# Compare
comparison_3 = expected_output_3 == actual_output_3
print(comparison_3)
print(f"Number of differences: {np.sum(comparison_3 == False)}")
