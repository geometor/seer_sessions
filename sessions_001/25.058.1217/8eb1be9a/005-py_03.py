import numpy as np

def get_azure_rows(grid):
    azure_rows = []
    for i, row in enumerate(grid):
        if 8 in row:
            azure_rows.append(i)
    return azure_rows

def extract_azure_pattern(grid, row_indices):
    patterns = []
    for row_index in row_indices:
        row = grid[row_index]
        pattern = []
        for col_index, pixel in enumerate(row):
            if pixel == 8:
                pattern.append((row_index,col_index))
        if (len(pattern) > 0):
            patterns.append(pattern)
    return patterns

def analyze_example(input_grid, output_grid, example_number):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    azure_rows_input = get_azure_rows(input_grid)
    azure_pattern_input = extract_azure_pattern(input_grid, azure_rows_input)

    azure_rows_output = get_azure_rows(output_grid)
    azure_pattern_output = extract_azure_pattern(output_grid, azure_rows_output)


    print(f"Example {example_number}:")
    print(f"  Input Azure Rows: {azure_rows_input}")
    print(f"  Input Azure Pattern: {azure_pattern_input}")
    print(f"  Expected Output Azure Rows: {azure_rows_output}")
    print(f"  Expected Output Azure Pattern: {azure_pattern_output}")
    print(f"  Input Dimensions: {input_grid.shape}")
    print(f"  Output Dimensions: {output_grid.shape}")
    print("-" * 20)


# Example Usage (Conceptual - for demonstration in dreamer mode)
task_examples = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
        ],
        "output": [
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
        ],
    },
     {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 8, 8, 0, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 8, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 0, 0, 0, 0, 0],
        ],
    },
]

for i, example in enumerate(task_examples):
    analyze_example(example["input"], example["output"], i + 1)