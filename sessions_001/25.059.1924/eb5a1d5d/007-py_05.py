def analyze_example(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    print(f"Input shape: {input_shape}, Output shape: {output_shape}")
    print(f"Input colors: {input_colors}, Output colors: {output_colors}")

    # Additional analysis could involve identifying objects and their properties
    # (size, position of bottom-right pixel, etc.)

# Hypothetical usage (assuming 'examples' is a list of (input, output) pairs)

example_data = [
    (np.array([[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 0, 8], [8, 8, 8, 8, 8, 8]]), np.array([[8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 0]])),
    (np.array([[8, 8, 8, 8, 8], [8, 8, 8, 1, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8]]), np.array([[8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 1]])),
    (np.array([[8, 8, 8, 8], [8, 8, 0, 8], [8, 8, 8, 8]]), np.array([[8, 8, 8], [8, 8, 8], [8, 8, 0]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 2, 8], [8, 8, 8, 8, 8, 8, 8]]), np.array([[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 2]]))
]
for i, (input_grid, output_grid) in enumerate(example_data):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
    print("---")