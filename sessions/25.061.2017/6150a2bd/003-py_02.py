import numpy as np
from typing import List, Tuple, Dict

def transform(input_grid):
    rows = len(input_grid)
    cols = len(input_grid[0])
    # Corrected output grid initialization: dimensions are swapped
    output_grid = np.zeros((cols, rows), dtype=int)

    for i in range(rows):
        for j in range(cols):
            output_grid[j][rows - 1 - i] = input_grid[i][j]

    return output_grid

def compare_grids(grid1: np.ndarray, grid2: np.ndarray) -> bool:
    """Compares two grids for equality."""
    return np.array_equal(grid1, grid2)

def calculate_metrics(task_examples):
    results = []
    for example in task_examples:
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)
        is_correct = compare_grids(expected_output_grid, predicted_output_grid)

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': predicted_output_grid.shape,
            'expected_output_shape': expected_output_grid.shape,
            'correct': is_correct
        })
    return results