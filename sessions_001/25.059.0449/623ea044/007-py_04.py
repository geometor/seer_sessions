def code_execution(input_grid, output_grid, transform_func):
    transformed_grid = transform_func(input_grid)
    comparison = np.array_equal(transformed_grid, output_grid)
    print(f"Input:\n{input_grid}\nExpected Output:\n{output_grid}\nTransformed:\n{transformed_grid}\nMatch: {comparison}")
    return comparison

# Example Usage (Hypothetical) - assuming 'train' is a list of (input, output) pairs
# Loop will be implicit in actual usage.
# Assuming train is available in the environment
# for input_grid, output_grid in train:
#     code_execution(input_grid, output_grid, transform)