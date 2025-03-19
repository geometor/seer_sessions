import numpy as np

# The provided transform function (included for completeness)
def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the locations of gray (5) pixels.  These remain unchanged.
    gray_pixels = np.where(input_grid == 5)

    # Find original red pixels in the bottom row
    bottom_row_red_pixels = np.where(input_grid[-1, :] == 2)[0]

    # Expand red upwards
    for col in bottom_row_red_pixels:
        output_grid[:, col] = 2

    # Gray Influence - horizontal spread of adjacent reds
    for r, c in zip(gray_pixels[0], gray_pixels[1]):
        if c > 0:
          if output_grid[r, c-1] == 0:
            output_grid[r, c - 1] = 2
        if c < cols - 1:
          if output_grid[r, c+1] == 0:
            output_grid[r, c + 1] = 2
    
    return output_grid

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0],
                           [0, 0, 2, 0, 0, 0]]),
        "output": np.array([[2, 2, 5, 2, 2, 2],
                            [2, 2, 5, 2, 2, 2],
                            [2, 2, 5, 2, 2, 2],
                            [2, 2, 5, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 0, 0, 5, 0],
                           [0, 0, 5, 0, 0, 5, 0],
                           [0, 0, 5, 0, 0, 5, 0],
                           [0, 0, 2, 0, 0, 2, 0]]),
        "output": np.array([[2, 2, 5, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 5, 2],
                            [2, 2, 2, 2, 2, 2, 2]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 5, 0, 0, 0, 5, 0],
                           [0, 0, 5, 0, 0, 0, 5, 0],
                           [0, 0, 5, 0, 0, 0, 5, 0],
                           [0, 0, 2, 0, 0, 0, 2, 0]]),
        "output": np.array([[2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 5, 2, 2, 2, 5, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]),
    },
]


for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    correct = np.array_equal(predicted_output, expected_output)
    diff = np.where(predicted_output != expected_output)
    print(f"Example {i + 1}: Correct = {correct}")
    if not correct:
        print("  Differences at (row, col):")
        for r, c in zip(diff[0], diff[1]):
            print(f"    ({r}, {c}) - Predicted: {predicted_output[r, c]}, Expected: {expected_output[r, c]}")