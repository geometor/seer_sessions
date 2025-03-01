import numpy as np

# Provided code (slightly modified for analysis)
def get_center(grid, size=3):
    """Helper function to extract a subgrid of given size from center of grid"""
    grid_rows, grid_cols = grid.shape
    center_row = grid_rows // 2
    center_col = grid_cols // 2
    
    start_row = center_row - size // 2
    end_row = center_row + size // 2 + 1  # Include the center row
    start_col = center_col - size // 2
    end_col = center_col + size // 2 + 1 # Include the center col    
    
    return grid[start_row:end_row, start_col:end_col]


def transform(input_grid):
    """Extracts the central 3x3 subgrid from the input grid."""
    # Convert the input grid to a NumPy array
    input_np = np.array(input_grid)

    # Get central 3 x 3
    output_grid = get_center(input_np, 3)

    return output_grid.tolist()

#Example data
train_ex = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0], [0, 7, 0], [0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0], [0, 7, 0], [0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0], [0, 7, 0], [0, 0, 0]]}
]
test_ex = [
    {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0], [0, 7, 0], [0, 0, 0]]}
]

for i, example in enumerate(train_ex):
    input_grid = example['input']
    expected_output = example['output']
    predicted_output = transform(input_grid)
    input_shape = np.array(input_grid).shape
    output_shape = np.array(expected_output).shape
    print(f"Example {i+1}:")
    print(f"  Input Shape: {input_shape}")
    print(f"  Expected Output Shape: {output_shape}")
    print(f"  Predicted Output Shape: {np.array(predicted_output).shape}")
    print(f"  Correct Prediction: {predicted_output == expected_output}")
    print("---")

for i, example in enumerate(test_ex):
    input_grid = example['input']
    expected_output = example['output']
    predicted_output = transform(input_grid)
    input_shape = np.array(input_grid).shape
    output_shape = np.array(expected_output).shape
    print(f"Test Example {i+1}:")
    print(f"  Input Shape: {input_shape}")
    print(f"  Expected Output Shape: {output_shape}")
    print(f"  Predicted Output Shape: {np.array(predicted_output).shape}")
    print(f"  Correct Prediction: {predicted_output == expected_output}")
    print("---")