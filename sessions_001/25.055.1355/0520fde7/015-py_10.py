import numpy as np

# Provided examples (replace with actual data loading if needed)
train_inputs = [
    np.array([[5, 0, 0], [5, 0, 0], [5, 1, 0], [5, 0, 0], [5, 0, 1]]),  # Example 1
    np.array([[5, 0, 0, 0], [5, 1, 0, 0], [5, 0, 0, 0], [5, 0, 1, 0], [5, 0, 0, 0]]),  # Example 2
    np.array([[0, 0, 5, 0, 0], [0, 5, 1, 0, 0], [5, 1, 0, 0, 0], [0, 5, 0, 0, 0], [0, 0, 5, 1, 0]]),  # Example 3
]
train_outputs = [
    np.array([[0, 0, 0], [0, 0, 0], [2, 0, 0]]),  # Example 1
    np.array([[0, 0, 0], [2, 0, 0], [0, 0, 0]]),  # Example 2
    np.array([[0, 0, 0], [0, 2, 0], [2, 0, 0]]),  # Example 3
]

def find_gray_stripe_column(grid):
    """Finds the column index of the vertical gray stripe."""
    for col in range(grid.shape[1]):
        if all(grid[:, col] == 5):
            return col
    return -1  # Should not happen based on problem description

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    # Initialize output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the gray stripe
    gray_stripe_col = find_gray_stripe_column(input_grid)

    # Process each row
    for row in range(input_grid.shape[0]):
        # Find blue pixels to the left and right of the gray stripe
        
        if gray_stripe_col > 0 and input_grid[row, gray_stripe_col - 1] == 1 :
            output_grid[row, (gray_stripe_col - 1) // 2 ] = 2

        if gray_stripe_col < input_grid.shape[1] - 1 and input_grid[row, gray_stripe_col + 1] == 1:
           output_grid[row,( gray_stripe_col + 1) // 2] = 2
           
    return output_grid

results = []
for i, (input_grid, expected_output) in enumerate(zip(train_inputs, train_outputs)):
    actual_output = transform(input_grid)
    
    gray_stripe_col = find_gray_stripe_column(input_grid)
    blue_pixels_left = []
    blue_pixels_right = []
    if gray_stripe_col != -1:  # If a gray stripe is found
        for row in range(input_grid.shape[0]):
            if gray_stripe_col > 0 and input_grid[row, gray_stripe_col - 1] == 1:
                blue_pixels_left.append((row, gray_stripe_col - 1))
            if gray_stripe_col < input_grid.shape[1] - 1 and input_grid[row, gray_stripe_col + 1] == 1:
                blue_pixels_right.append((row, gray_stripe_col + 1))


    metrics = {
        'example': i + 1,
        'input_shape': input_grid.shape,
        'output_shape': expected_output.shape,
        'gray_stripe_col': gray_stripe_col,
        'blue_pixels_left': blue_pixels_left,
        'blue_pixels_right': blue_pixels_right,
        'expected_output': expected_output.tolist(),  # Convert to list for easier viewing
        'actual_output': actual_output.tolist(),      # Convert to list for easier viewing
        'correct': np.array_equal(actual_output, expected_output)
    }
    results.append(metrics)

for r in results:
    print(r)