import numpy as np

def describe_grid(grid):
    """Provides a description of the grid, including non-white pixel locations and colors."""
    rows, cols = grid.shape
    description = {
        'shape': (rows, cols),
        'colors': {},
        'color_positions': {}
    }
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                if color not in description['colors']:
                    description['colors'][color] = 0
                description['colors'][color] += 1
                if color not in description['color_positions']:
                    description['color_positions'][color] = []
                description['color_positions'][color].append((r,c))
    return description
def compare_grids(input, predicted, target):
    """
        Compares the input, predicted, and target output
    """
    return {
        'input': describe_grid(input),
        'predicted' : describe_grid(predicted),
        'target': describe_grid(target)
    }

# Example Usage (replace with actual grids from the task)
task_examples = [
    {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output': np.array([[0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0]]),
    },
    {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output': np.array([[0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0]]),
    },
    {
       'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output': np.array([[0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0]]),
    },
]

from previous_code_snippet import transform

results = []

for example in task_examples:
    input_grid = example['input']
    target_output_grid = example['output']
    predicted_output_grid = transform(input_grid)
    results.append(compare_grids(input_grid, predicted_output_grid, target_output_grid))

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input: {result['input']}")
    print(f"  Predicted Output: {result['predicted']}")
    print(f"  Target Output: {result['target']}")
    print("-" * 20)
