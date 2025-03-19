input_grid = [[8, 3, 8, 3, 8, 8, 3, 8, 3, 8, 3, 8, 3], [8, 3, 8, 3, 8, 8, 3, 8, 3, 8, 3, 8, 3], [8, 3, 8, 3, 8, 8, 3, 8, 3, 8, 3, 8, 3], [8, 3, 8, 3, 8, 8, 3, 8, 3, 8, 3, 8, 3], [8, 3, 8, 3, 8, 8, 3, 8, 3, 8, 3, 8, 3]]
expected_output = [[8, 3, 8, 3, 8], [8, 3, 8, 3, 8], [8, 3, 8, 3, 8], [8, 3, 8, 3, 8], [8, 3, 8, 3, 8]]
output_grid = transform(input_grid)

print(f"expected_output: {expected_output}")
print(f"output_grid    : {output_grid}")

input_grid = np.array(input_grid)
rows, cols = input_grid.shape
expected_grid = np.array(expected_output)
expected_rows, expected_cols = expected_grid.shape
output_grid = np.array(output_grid)
output_rows, output_cols = output_grid.shape

print(f"input shape: {input_grid.shape}")
print(f"output shape: {expected_grid.shape}")
print(f"result shape: {output_grid.shape}")
print(f"result matches expected: {np.array_equal(output_grid, expected_grid)}")