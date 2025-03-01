import numpy as np

def find_largest_connected_region(grid, color):
    """Finds the largest connected region of a given color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    max_region = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                if len(current_region) > len(max_region):
                    max_region = current_region
    return max_region

def transform(input_grid):
    # Find the largest connected region of blue (1) pixels.
    blue_region = find_largest_connected_region(input_grid, 1)

    if not blue_region:
        return np.array([[1]]) # handle edge case with no blue.

    # Determine the bounding box of the blue region.
    min_row = min(r for r, c in blue_region)
    max_row = max(r for r, c in blue_region)
    min_col = min(c for r, c in blue_region)
    max_col = max(c for r, c in blue_region)

    # Determine output grid dimensions.
    output_width = 6
    output_height = 5 if (max_row - min_row + 1) > 1 else 3

    # Create the output grid with a checkerboard pattern.
    output_grid = np.zeros((output_height, output_width), dtype=int)
    for row in range(output_height):
        for col in range(output_width):
            # Calculate checkerboard pattern based on the top-left of the blue region.
            if (row + col - min_row - min_col) % 2 == 0:
                 # Offset by min_row and min_col to align checkerboard
                output_grid[row, col] = 1  # Blue
            else:
                output_grid[row, col] = 2  # Red

    return output_grid

# Example Usage (modified for debugging/analysis):
task_id = '63613498'
train_or_test = 'train'
i = 0

input_grid = np.array(eval(input()))  # Dynamically input the grid
expected_output = np.array(eval(input()))

predicted_output = transform(input_grid)

blue_region = find_largest_connected_region(input_grid, 1)
min_row, max_row = -1, -1
min_col, max_col = -1, -1
if blue_region:
  min_row = min(r for r, c in blue_region)
  max_row = max(r for r, c in blue_region)
  min_col = min(c for r, c in blue_region)
  max_col = max(c for r, c in blue_region)


print(f"Example {i+1}:")
print(f"  Input Grid Dimensions: {input_grid.shape}")
print(f"  Expected Output Dimensions: {expected_output.shape}")
print(f"  Predicted Output Dimensions: {predicted_output.shape}")
print(f"  Blue Region: {blue_region}")
print(f"  min_row: {min_row}, max_row: {max_row}, min_col: {min_col}, max_col: {max_col}")
print(f"  Blue Region Height: {max_row - min_row + 1 if blue_region else 0}")
print(f"  Expected Output:\n{expected_output}")
print(f"  Predicted Output:\n{predicted_output}")
print(f"  Correct Prediction: {np.array_equal(expected_output, predicted_output)}")