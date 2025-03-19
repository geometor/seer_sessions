import numpy as np

def analyze_results(input_grid, expected_output, actual_output):
    mismatches = np.where(expected_output != actual_output)
    num_mismatches = len(mismatches[0])
    print(f"Number of mismatches: {num_mismatches}")

    if num_mismatches > 0:
        print("Mismatch coordinates and values:")
        for i in range(num_mismatches):
            row = mismatches[0][i]
            col = mismatches[1][i]
            print(f"  Row: {row}, Col: {col}, Expected: {expected_output[row, col]}, Actual: {actual_output[row, col]}, Input: {input_grid[row,col]}")

# Provided examples
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 9, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0]]),
    },
]

def transform(input_grid):
    """
    Transforms the input grid by expanding each non-zero pixel into a horizontal
    and vertical line of the same color.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find non-zero pixels
    non_zero_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append((r, c, input_grid[r, c]))

    # Expand each non-zero pixel
    for r, c, value in non_zero_pixels:
        # Horizontal expansion
        for i in range(cols):
            output_grid[r, i] = value

        # Vertical expansion
        for i in range(rows):
            output_grid[i, c] = value

    return output_grid

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    actual_output = transform(example["input"].copy()) # Use a copy to avoid modifying the original input.
    analyze_results(example["input"], example["output"], actual_output)
    print("-" * 20)
