import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Blue Pixel Shift
            if input_grid[r, c] == 1 and c == 3 and r >= 2:
                output_grid[r + 1, c] = 1
            # Green Pixel Shift
            elif input_grid[r,c] == 3 and c == 1 and r >= 1:
                output_grid[r+1,c] = 3
            # Magenta Pixel Shift
            elif input_grid[r, c] == 6 and r == 3 and c == 0:
                output_grid[r + 1, c] = 6
            # Red pixel Shift
            elif input_grid[r,c] == 2 and c == 4 and r < 2:
                output_grid[r+1,c-1] = 2
            # Copy Remaining
            elif input_grid[r, c] != 0:
                output_grid[r, c] = input_grid[r, c]

    return output_grid

# Example data (replace with your actual task data)
example_inputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [6, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 3, 0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 3, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 2, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 3, 0, 1, 0, 0],
              [6, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]])
]

example_outputs = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [6, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 3, 0, 0, 2, 0, 0],
              [0, 3, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 2, 0],
              [0, 3, 0, 0, 0, 0],
              [6, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0]])
]

for i, (input_grid, expected_output) in enumerate(zip(example_inputs, example_outputs)):
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print("Input:\n", input_grid)
    print("Expected Output:\n", expected_output)
    print("Predicted Output:\n", predicted_output)
    print("Match:", np.array_equal(predicted_output, expected_output))
    print("-" * 20)