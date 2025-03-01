import numpy as np

def analyze_grid(grid, label):
    """Analyzes a single grid and prints relevant information."""
    print(f"--- {label} ---")
    print(f"  Dimensions: {grid.shape}")
    unique_colors = np.unique(grid)
    print(f"  Unique Colors: {unique_colors}")
    for color in unique_colors:
        count = np.sum(grid == color)
        print(f"  Color {color} Count: {count}")

def transform(input_grid):

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Swap color 2 with color 6 and vice versa.
    output_grid[input_grid == 2] = 6
    output_grid[input_grid == 6] = 2

    return output_grid

# Provided training examples
train_examples = [
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
    },
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 2, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 6, 5, 5, 5, 5]],
    },
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 6, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 2, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
    },
    {
        "input": [[6, 5, 5, 5, 5, 5, 5, 5, 5, 2],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[2, 5, 5, 5, 5, 5, 5, 5, 5, 6],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                   [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
    },
]

# Convert examples to numpy arrays
train_examples_np = [
    {"input": np.array(ex["input"]), "output": np.array(ex["output"])}
    for ex in train_examples
]

# Analyze each example
for i, example in enumerate(train_examples_np):
    analyze_grid(example["input"], f"Example {i+1} Input")
    analyze_grid(example["output"], f"Example {i+1} Output")
    predicted_output = transform(example["input"])
    analyze_grid(predicted_output, f"Example {i+1} Predicted Output")
    print(f"Match: {np.array_equal(predicted_output, example['output'])}\n")
