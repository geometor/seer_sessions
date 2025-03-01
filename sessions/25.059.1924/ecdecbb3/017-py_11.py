import numpy as np

def describe_grid(grid, grid_name):
    """Provides a basic description of a grid."""
    rows, cols = grid.shape
    unique_values = np.unique(grid)
    print(f"{grid_name}:")
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Unique values: {unique_values}")
    # additional checks
    for value in unique_values:
      print(f'  pixels with {value=}: {np.count_nonzero(grid == value)}')

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    print("--- Analyzing Example ---")
    describe_grid(input_grid, "Input Grid")
    describe_grid(output_grid, "Output Grid")
    print("-" * 30)

# Assuming 'train' is a list of dictionaries, each with 'input' and 'output'
train = task["train"]

for i, example in enumerate(train):
    print(f"*** Example {i + 1} ***")
    analyze_example(np.array(example['input']), np.array(example['output']))
