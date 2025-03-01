import numpy as np

def find_blue_pixel(grid):
    # Find the coordinates of the blue pixel (value 1).
    for r_idx, row in enumerate(grid):
        for c_idx, val in enumerate(row):
            if val == 1:
                return (r_idx, c_idx)
    return None  # Should not happen in this specific task, but good practice.

def calculate_metrics(input_grid, output_grid, predicted_grid):
    blue_pixel_input = find_blue_pixel(input_grid)
    blue_pixel_output = find_blue_pixel(output_grid)
    
    metrics = {
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape,
        'blue_pixel_input': blue_pixel_input,
        'blue_pixel_output': blue_pixel_output,
        'predicted_output_match': np.array_equal(output_grid, predicted_grid)
    }
    return metrics
    

def transform(input_grid):
    """
    Transforms the input grid as per the described rules.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output grid with the same dimensions.
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Locate the blue pixel in the input grid.
    blue_row, blue_col = find_blue_pixel(input_grid)

    # Populate the output grid.
    for r_idx in range(height):
        # Determine the starting value for the alternating pattern.
        if (blue_col + r_idx) % 2 == 0:
            start_val = 8
        else:
            start_val = 1

        # Fill the row with the alternating pattern.
        for c_idx in range(width):
            if (c_idx % 2) == 0:
               output_grid[r_idx, c_idx] = start_val
            elif start_val == 8:
                output_grid[r_idx, c_idx] = 1
            else:
                output_grid[r_idx,c_idx] = 8

    return output_grid

# Provided examples
train_input_0 = np.array([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
train_output_0 = np.array([[8, 1, 8, 1, 8, 1, 8], [1, 8, 1, 8, 1, 8, 1], [8, 1, 8, 1, 8, 1, 8], [1, 8, 1, 8, 1, 8, 1], [8, 1, 8, 1, 8, 1, 8], [1, 8, 1, 8, 1, 8, 1], [8, 1, 8, 1, 8, 1, 8]])
train_input_1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
train_output_1 = np.array([[1, 8, 1, 8, 1, 8, 1, 8], [8, 1, 8, 1, 8, 1, 8, 1], [1, 8, 1, 8, 1, 8, 1, 8], [8, 1, 8, 1, 8, 1, 8, 1], [1, 8, 1, 8, 1, 8, 1, 8], [8, 1, 8, 1, 8, 1, 8, 1], [1, 8, 1, 8, 1, 8, 1, 8], [8, 1, 8, 1, 8, 1, 8, 1]])
train_input_2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_2 = np.array([[8, 1, 8, 1, 8, 1, 8, 1, 8], [1, 8, 1, 8, 1, 8, 1, 8, 1], [8, 1, 8, 1, 8, 1, 8, 1, 8], [1, 8, 1, 8, 1, 8, 1, 8, 1], [8, 1, 8, 1, 8, 1, 8, 1, 8], [1, 8, 1, 8, 1, 8, 1, 8, 1], [8, 1, 8, 1, 8, 1, 8, 1, 8], [1, 8, 1, 8, 1, 8, 1, 8, 1], [8, 1, 8, 1, 8, 1, 8, 1, 8]])

# Gather metrics
predicted_output_0 = transform(train_input_0)
metrics_0 = calculate_metrics(train_input_0, train_output_0, predicted_output_0)
predicted_output_1 = transform(train_input_1)
metrics_1 = calculate_metrics(train_input_1, train_output_1, predicted_output_1)
predicted_output_2 = transform(train_input_2)
metrics_2 = calculate_metrics(train_input_2, train_output_2, predicted_output_2)


print(f"Metrics for Example 0:\n{metrics_0}\n")
print(f"Metrics for Example 1:\n{metrics_1}\n")
print(f"Metrics for Example 2:\n{metrics_2}\n")