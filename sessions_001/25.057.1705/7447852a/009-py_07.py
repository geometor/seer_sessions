import numpy as np

def describe_grid(grid):
    """Provides a descriptive summary of the grid."""
    rows, cols = grid.shape
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    description = {
        "dimensions": f"{rows}x{cols}",
        "colors": color_counts
    }
    return description

def analyze_examples(examples):
   report = ""
   for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        transformed_grid = transform(input_grid)  # use the provided transform
        correct = np.array_equal(output_grid, transformed_grid)
        
        report += f"Example {i+1}:\n"
        report += f"  Input: {describe_grid(input_grid)}\n"
        report += f"  Output: {describe_grid(output_grid)}\n"
        report += f"  Transformed: {describe_grid(transformed_grid)}\n"
        report += f"  Correct: {correct}\n"
        report += "\n"
   return report

# ARC-FORMATTED EXAMPLES:
examples = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [2, 4, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 2, 4], [0, 0, 0, 0, 0, 2, 4, 0], [0, 0, 0, 0, 2, 4, 0, 0], [0, 0, 0, 2, 4, 0, 0, 0], [0, 0, 2, 4, 0, 0, 0, 0], [0, 2, 4, 0, 0, 0, 0, 0], [2, 4, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2]], 'output': [[2, 4, 2, 4, 2, 4, 2, 4], [0, 2, 4, 2, 4, 2, 4, 2]]}
    ]

print(analyze_examples(examples))