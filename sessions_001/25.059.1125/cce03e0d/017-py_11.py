import numpy as np

def analyze_example(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    input_pixels = np.count_nonzero(input_grid)
    output_pixels = np.count_nonzero(output_grid)
    print(f"  Input shape: {input_shape}")
    print(f"  Output shape: {output_shape}")
    print(f"  Input non-zero pixels: {input_pixels}")
    print(f"  Output non-zero pixels: {output_pixels}")
    print(f"Output Pixels / Input Pixels:{output_pixels/input_pixels}")

# Dummy data for demonstration - replace with actual data loading
train_examples = [
    (np.array([[1, 2], [3, 4]]), np.array([[1, 2, 0, 1, 2], [3, 4, 0, 3, 4], [0, 0, 0, 0, 0], [1, 2, 0, 1, 2], [3, 4, 0, 3, 4]])),  # Example 1 (assuming this was the original)
    (np.array([[5, 6, 7], [8, 9, 1]]), np.array([[5, 6, 7, 5, 6, 7], [8, 9, 1, 8, 9, 1], [5, 6, 7, 5, 6, 7], [8, 9, 1, 8, 9, 1]])),  # Example 2
    (np.array([[2]]), np.array([[2, 2], [2, 2]])),  # Example 3
]

for i, (input_grid, output_grid) in enumerate(train_examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
