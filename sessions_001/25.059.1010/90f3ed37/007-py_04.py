import numpy as np

def find_horizontal_blocks(grid, color):
    blocks = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = None
        for c in range(cols):
            if grid[r, c] == color:
                if start_col is None:
                    start_col = c
            elif start_col is not None:
                blocks.append(((r, start_col), (r, c - 1)))
                start_col = None
        if start_col is not None:
            blocks.append(((r, start_col), (r, cols - 1)))
    return blocks

def analyze_example(input_grid, expected_output, actual_output):
    azure_blocks_input = find_horizontal_blocks(input_grid, 8)
    blue_blocks_expected = find_horizontal_blocks(expected_output, 1)
    blue_blocks_actual = find_horizontal_blocks(actual_output, 1)

    discrepancies = np.where(expected_output != actual_output)


    print("Azure Blocks in Input:", azure_blocks_input)
    print("Blue Blocks in Expected Output:", blue_blocks_expected)
    print("Blue Blocks in Actual Output:", blue_blocks_actual)
    print("Discrepancy Locations (Expected != Actual):", discrepancies)
    print("-" * 20)

# define grids for example data
train_ex_inputs = [
    np.array([[5, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 8, 8, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [8, 8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
]

train_ex_outputs = [
    np.array([[5, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 8, 8, 8, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 0, 0]]),
    np.array([[0, 5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [8, 8, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
]

# get transform results
train_ex_results = []
for input_grid in train_ex_inputs:
  train_ex_results.append(transform(input_grid))

# Analyze each example
for i in range(len(train_ex_inputs)):
    print(f"Example {i+1}:")
    analyze_example(train_ex_inputs[i], train_ex_outputs[i], train_ex_results[i])