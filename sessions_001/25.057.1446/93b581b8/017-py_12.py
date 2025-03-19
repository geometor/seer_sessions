import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    unique_values = np.unique(grid)
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Unique values: {unique_values}")

def analyze_example(input_grid, output_grid):
    print("Input Grid:")
    describe_grid(input_grid)
    print("Output Grid:")
    describe_grid(output_grid)
    # additional analysis as needed, comparing input and output.

# Example Usage (assuming input_grid and output_grid are available from the first training example)
# analyze_example(input_grid, output_grid)

# Load the training data for all examples, not just the first
import json
from pathlib import Path

data_path = Path('../data/training')
task_file = data_path / '0b17322b.json'

with open(task_file, 'r') as f:
    task = json.load(f)

train_examples = task['train']

for i, example in enumerate(train_examples):
    print(f"--- Example {i+1} ---")
    analyze_example(np.array(example['input']), np.array(example['output']))
