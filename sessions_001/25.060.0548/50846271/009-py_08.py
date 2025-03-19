# Example setup (replace with actual grid data loading)
def get_task_examples():
    #simplified for this response
    return [
      # 0
        ([
            [5, 5, 5, 5, 5],
            [5, 2, 5, 2, 5],
            [5, 5, 5, 5, 5],
            [5, 2, 5, 2, 5],
            [5, 5, 5, 5, 5]
        ],
        [
            [5, 5, 5, 5, 5],
            [5, 8, 5, 8, 5],
            [5, 5, 5, 5, 5],
            [5, 8, 5, 8, 5],
            [5, 5, 5, 5, 5]
        ]),
        # 1
        ([
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 2, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 2, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
        ],
        [
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 2, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 2, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
        ]),
        # 2
        ([
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ],
        [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 8, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ])
    ]

def execute_previous_code(input_grid):
    """
    Placeholder for running the previously generated code.
    """
    # Replaces red (2) pixels with azure (8) pixels if the red pixel is
    # surrounded by exactly four gray (5) pixels (up, down, left, and right).
    # Other pixels remain unchanged.

    import numpy as np

    def transform(input_grid):
        output_grid = np.copy(input_grid)  # Create a copy to modify
        rows, cols = input_grid.shape

        # Iterate through each pixel
        for r in range(rows):
            for c in range(cols):
                # Check if the current pixel is red (2)
                if input_grid[r, c] == 2:
                    # Count gray neighbors (up, down, left, right)
                    gray_neighbors = 0
                    if r > 0 and input_grid[r - 1, c] == 5:  # Up
                        gray_neighbors += 1
                    if r < rows - 1 and input_grid[r + 1, c] == 5:  # Down
                        gray_neighbors += 1
                    if c > 0 and input_grid[r, c - 1] == 5:  # Left
                        gray_neighbors += 1
                    if c < cols - 1 and input_grid[r, c + 1] == 5:  # Right
                        gray_neighbors += 1

                    # If exactly four gray neighbors, change to azure (8)
                    if gray_neighbors == 4:
                        output_grid[r, c] = 8

        return output_grid

    return transform(np.array(input_grid))

def compare_grids(grid1, grid2):
    """Compares two grids and returns the differences."""
    return (np.array(grid1) != np.array(grid2)).sum()

examples = get_task_examples()
print("Example Results:")
for i, (input_grid, expected_output) in enumerate(examples):
    predicted_output = execute_previous_code(input_grid)
    differences = compare_grids(predicted_output, expected_output)
    print(f"Example {i}: Differences = {differences}")

# Test Set
print("Test Set:")
test_input = ([
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 2, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
        ],
        [
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 8, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
        ])
predicted_test_output = execute_previous_code(test_input[0])
test_differences = compare_grids(predicted_test_output, test_input[1])
print(f"Test Case: Differences = {test_differences}")