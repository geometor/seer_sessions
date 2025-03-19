import numpy as np

# Provided code (slightly modified for output)

def get_non_black_color(grid):
    """Finds the non-black color in a grid."""
    colors = np.unique(grid)
    for color in colors:
        if color != 0:
            return color
    return 0  # Return 0 if only black is present

def transform(input_grid):
    # Initialize the output grid. Dimensions are half the input, rounded up.
    input_rows, input_cols = input_grid.shape
    output_rows = (input_rows + 1) // 2
    output_cols = (input_cols + 1) // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Identify the non-black color in the input grid.
    target_color = get_non_black_color(input_grid)

    # Iterate through odd rows and columns of the input grid.
    for i in range(0, input_rows, 2):
        for j in range(0, input_cols, 2):
            # Map input indices to output indices (integer division by 2).
            output_i = i // 2
            output_j = j // 2

            # Copy the pixel value if it matches the target color.
            if input_grid[i, j] == target_color:
                output_grid[output_i, output_j] = target_color

    return output_grid

# Task Examples (Replace with actual data)
task_examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 7, 0, 7, 0, 7],
                           [0, 0, 0, 0, 0, 0],
                           [0, 7, 0, 7, 0, 7],
                           [0, 0, 0, 0, 0, 0],
                           [0, 7, 0, 7, 0, 7]]),
        "output": np.array([[7, 7, 7],
                            [7, 7, 7],
                            [7, 7, 7]])
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 0, 1, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 0, 1, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 0, 1, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                           [0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                           [0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 8, 8, 8, 8, 8],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]])
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0],
                           [0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0],
                           [0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 6, 6, 6, 6, 6],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]])
    },


]

for i, example in enumerate(task_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)

    print(f"Example {i+1}:")
    print("Input:")
    print(input_grid)
    print("Expected Output:")
    print(expected_output)
    print("Predicted Output:")
    print(predicted_output)
    print(f"Input Shape: {input_grid.shape}")
    print(f"Expected Output Shape: {expected_output.shape}")
    print(f"Predicted Output Shape: {predicted_output.shape}")
    print("-" * 20)