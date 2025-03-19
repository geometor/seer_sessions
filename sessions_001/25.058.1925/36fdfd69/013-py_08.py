import numpy as np

def analyze_red_pixels(grid, description):
    """Analyzes the red pixels in a grid and their neighbors."""
    rows, cols = grid.shape
    red_pixel_count = 0
    red_pixels_with_non_red_neighbors = 0
    red_pixels_all_red_neighbors = 0
    
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 2:
                red_pixel_count += 1
                adjacent_values = get_adjacent_pixels(grid, row, col)
                if any(val != 2 for val in adjacent_values):
                    red_pixels_with_non_red_neighbors += 1
                else:
                    red_pixels_all_red_neighbors += 1

    print(f"Analysis of {description}:")
    print(f"  Total Red Pixels: {red_pixel_count}")
    print(f"  Red Pixels with Non-Red Neighbors: {red_pixels_with_non_red_neighbors}")
    print(f"  Red Pixels with All-Red Neighbors: {red_pixels_all_red_neighbors}")
    print("-" * 40)


def compare_grids(input_grid, expected_output, actual_output):
    """Compares the expected and actual outputs, highlighting differences."""
    print("Comparison of Expected vs. Actual Output:")
    rows, cols = input_grid.shape
    differences = 0
    for row in range(rows):
        for col in range(cols):
            if expected_output[row,col] != actual_output[row,col]:
                differences += 1
                print(f"  Difference at ({row}, {col}): Expected {expected_output[row, col]}, Actual {actual_output[row, col]}")
    print(f"Total Differences: {differences}")
    print("-" * 40)

# Example Data (Replace with actual data loading)
# example_data = [
#     (np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]]), np.array([[0, 0, 0], [0, 4, 0], [0, 0, 0]])),
#     (np.array([[2, 2, 2], [2, 2, 2], [2, 2, 2]]), np.array([[2, 2, 2], [2, 2, 2], [2, 2, 2]])),
#     (np.array([[0, 2, 0], [2, 2, 2], [0, 2, 0]]), np.array([[0, 4, 0], [4, 2, 4], [0, 4, 0]])),
# ]

# provided in next turn
example_data = task_data['train']

for i, (input_grid, expected_output) in enumerate(example_data):
    actual_output = transform(input_grid)
    
    analyze_red_pixels(input_grid, f"Input Grid {i+1}")
    analyze_red_pixels(expected_output, f"Expected Output Grid {i+1}")
    analyze_red_pixels(actual_output, f"Actual Output Grid {i+1}")

    compare_grids(input_grid, expected_output, actual_output)
