import numpy as np
from typing import List, Tuple

def grid_report(grid: np.ndarray) -> Tuple[List[Tuple[int,int,int]], int, int]:
    """Generates a report about the objects within a grid.
    Returns:
        Tuple: (color_counts, rows, cols) where:
        color_counts is a list of (color, occurrences, area)
    """

    rows, cols = grid.shape
    unique_colors = np.unique(grid)

    color_counts = []
    for color in unique_colors:
        count = np.sum(grid == color)
        color_counts.append((int(color), count, count)) # color, occurrences, area

    return color_counts, rows, cols

def print_grid(grid):
    for row in grid:
        print("".join(map(str, row)))

def process_task(task):
    print("Task:", task['name'])
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)
        print("\nInput:")
        print_grid(input_grid)
        input_report, _, _ = grid_report(input_grid)
        print("Input Report:", input_report)
        
        print("\nExpected Output:")
        print_grid(output_grid)
        output_report,_,_ = grid_report(output_grid)
        print("Output Report:", output_report)
        
        print("\nPredicted Output:")
        print_grid(predicted_output)
        predicted_report,_,_ = grid_report(predicted_output)
        print("Predicted Report:", predicted_report)
        
        print("\nComparison (Expected == Predicted):")
        print(np.array_equal(output_grid, predicted_output))

# "hard-coded" the task dictionary - normally acquired via JSON parsing
task = {
    "name":
    "3ed85e60",
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 3, 0, 0, 0, 3, 0, 0], [0, 0, 3, 0, 0, 0, 3, 0, 0], [0, 0, 3, 0, 0, 0, 3, 0, 0], [0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 3, 0, 0, 0], [0, 0, 0, 3, 0, 0, 3, 0, 0, 0], [0, 0, 0, 3, 0, 0, 3, 0, 0, 0], [0, 0, 0, 3, 0, 0, 3, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
    ]
}
process_task(task)