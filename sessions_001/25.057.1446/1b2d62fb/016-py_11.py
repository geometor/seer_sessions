import numpy as np

def analyze_results(train_set, transform_func):
    results = []
    for i, (input_grid, expected_output) in enumerate(train_set):
        input_np = np.array(input_grid)
        expected_np = np.array(expected_output)
        actual_output = transform_func(input_grid)  # Assuming 'transform' is defined
        actual_np = np.array(actual_output)

        # Find the column index of the blue line (all 1s)
        blue_line_col = -1
        for col_idx in range(input_np.shape[1]):
            if np.all(input_np[:, col_idx] == 1):
                blue_line_col = col_idx
                break

        results.append({
            "example_index": i,
            "input_shape": input_np.shape,
            "expected_output_shape": expected_np.shape,
            "actual_output_shape": actual_np.shape,
            "blue_line_col": blue_line_col,
            "matches_expected": np.array_equal(expected_np, actual_np)
        })
    return results
def transform(grid):
    """
    Initial transform function - replaces 1s with 8s
    """
    
    grid_np = np.array(grid)
    new_grid = np.where(grid_np == 1, 8, grid_np)
    
    # Find the column index of the blue line (all 1s)
    blue_line_col = -1
    for col_idx in range(new_grid.shape[1]):
        if np.all(new_grid[:, col_idx] == 8):
            blue_line_col = col_idx
            break
            
    if blue_line_col != -1:
        # Attempt to construct the output grid based on surrounding context
        output_grid = np.zeros_like(new_grid)
        rows, cols = new_grid.shape

        for r in range(rows):
            for c in range(cols):
                if c < blue_line_col:  # Left of blue line
                    if new_grid[r,c] !=0 and new_grid[r,c]!=1:
                        output_grid[r,c] = 8
                elif c > blue_line_col:  # Right of blue line
                    if new_grid[r,c] !=0 and new_grid[r,c]!=1:
                        output_grid[r,c] = 8


        return output_grid.tolist()
    else:
        return new_grid.tolist()  # Return original with 1s replaced

# Assuming 'train' variable holds the training examples
# Example usage (replace with actual 'train' data):
train = [
    (
        [[0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [9, 9, 9, 1, 9, 9, 9], [9, 9, 9, 1, 9, 9, 9], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]],
        [[8, 0, 8], [8, 0, 8], [0, 0, 0], [0, 0, 0], [8, 0, 8], [8, 0, 8]],
    ),
    (
        [[0, 0, 9, 9, 0, 0, 0], [0, 0, 9, 9, 0, 0, 0], [9, 9, 1, 1, 9, 9, 9], [0, 0, 1, 1, 0, 0, 0], [9, 9, 9, 9, 9, 9, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [8, 0, 8], [0, 0, 0]],
    ),
    (
        [[9, 9, 1, 9, 9], [9, 9, 1, 9, 9], [9, 9, 1, 9, 9]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ),
    (
      [[0, 9, 9, 9, 9, 0], [0, 9, 9, 9, 9, 0], [0, 9, 1, 9, 9, 0], [0, 9, 1, 9, 9, 0], [0, 9, 9, 9, 9, 0]],
      [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    ),
    (
        [[0, 9, 9, 0, 0, 0], [0, 0, 9, 9, 0, 0], [0, 0, 9, 9, 9, 0]],
        [[0, 9, 9, 0, 0, 0], [0, 0, 9, 9, 0, 0], [0, 0, 9, 9, 9, 0]],
    )
]

analysis = analyze_results(train, transform)
for result in analysis:
    print(result)