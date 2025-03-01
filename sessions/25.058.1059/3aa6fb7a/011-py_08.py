import numpy as np

def count_adjacent_azure(grid, row, col):
    """Counts the number of adjacent azure pixels (excluding diagonals)."""
    count = 0
    rows, cols = grid.shape
    # Check North
    if row > 0 and grid[row-1, col] == 8:
        count += 1
    # Check South
    if row < rows - 1 and grid[row+1, col] == 8:
        count += 1
    # Check West
    if col > 0 and grid[row, col-1] == 8:
        count += 1
    # Check East
    if col < cols - 1 and grid[row, col+1] == 8:
        count += 1
    return count

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is azure
            if input_grid[row, col] == 8:
                # Count adjacent azure pixels
                adjacent_count = count_adjacent_azure(input_grid, row, col)
                # Replace with blue if only one adjacent azure pixel
                if adjacent_count == 1:
                    output_grid[row, col] = 1

    return output_grid

def analyze_example(input_grid, expected_output_grid):
    transformed_grid = transform(input_grid)
    correct_count = np.sum(transformed_grid == expected_output_grid)
    incorrect_count = np.sum(transformed_grid != expected_output_grid)
    total_pixels = transformed_grid.size
    azure_pixels_input = np.sum(input_grid == 8)
    azure_to_blue_expected = np.sum((input_grid == 8) & (expected_output_grid == 1))
    azure_to_blue_actual = np.sum((input_grid == 8) & (transformed_grid == 1))
    return {
        "correct_pixels": int(correct_count),
        "incorrect_pixels": int(incorrect_count),
        "total_pixels": int(total_pixels),
        "accuracy": float(correct_count / total_pixels),
        "azure_pixels_input": int(azure_pixels_input),
        "azure_to_blue_expected": int(azure_to_blue_expected),
        "azure_to_blue_actual": int(azure_to_blue_actual),
        'transform_matches_expected': bool(np.array_equal(transformed_grid, expected_output_grid))
    }

# Example data (replace with your actual data)
example_data = [
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
       [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8]]),
np.array([[8, 8, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 1, 8, 1, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 1, 8, 1, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 1, 8, 1, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 8, 8, 8, 8, 8]])),
    (np.array([[8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
np.array([[8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 5, 8, 1, 8, 1, 8, 8],
       [8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 5, 8, 1, 8, 1, 8, 8],
       [8, 8, 8, 5, 8, 8, 8, 8, 8, 8],
       [8, 1, 8, 5, 8, 1, 8, 1, 8, 8],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]))
]

results = [analyze_example(inp, exp) for inp, exp in example_data]
for i, result in enumerate(results):
    print(f"Example {i+1}:")
    for key, value in result.items():
        print(f"  {key}: {value}")