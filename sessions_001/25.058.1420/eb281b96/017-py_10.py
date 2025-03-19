import numpy as np

def analyze_row_expansion(input_grid, output_grid):
    """
    Analyzes the row expansion between input and output grids.

    Args:
        input_grid: The input grid (list of lists).
        output_grid: The output grid (list of lists).

    Returns:
        A list of expansion factors, one for each row in the input grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    input_height = input_grid.shape[0]
    output_height = output_grid.shape[0]

    expansion_factors = []
    output_row_index = 0
    for input_row_index in range(input_height):
        expansion_count = 0
        while output_row_index < output_height and np.array_equal(output_grid[output_row_index], input_grid[input_row_index]):
            expansion_count += 1
            output_row_index += 1
        expansion_factors.append(expansion_count)


    return expansion_factors

# Example Usage (using provided task examples):
task_id = '3ed85e60'
train_examples = [
    {
        "input": [[0, 2, 0], [2, 0, 2], [0, 2, 0], [2, 2, 2]],
        "output": [[0, 2, 0], [0, 2, 0], [0, 2, 0], [2, 0, 2], [2, 0, 2], [0, 2, 0], [0, 2, 0], [2, 2, 2], [2, 2, 2], [2, 2, 2]],
    },
    {
        "input": [[8, 8, 8, 8], [0, 0, 0, 0], [8, 8, 8, 8], [0, 0, 0, 0]],
        "output": [[8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [0, 0, 0, 0], [0, 0, 0, 0], [8, 8, 8, 8], [8, 8, 8, 8], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    },
    {
        "input": [[6, 1, 1, 6, 1], [1, 6, 6, 1, 6], [6, 1, 1, 6, 1]],
        "output": [[6, 1, 1, 6, 1], [6, 1, 1, 6, 1], [6, 1, 1, 6, 1], [1, 6, 6, 1, 6], [1, 6, 6, 1, 6], [6, 1, 1, 6, 1], [6, 1, 1, 6, 1]],
    }
]


for i, example in enumerate(train_examples):
    print(f"Example {i+1}:")
    expansion_factors = analyze_row_expansion(example["input"], example["output"])
    print(f"  Expansion Factors: {expansion_factors}")
