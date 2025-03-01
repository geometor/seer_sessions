import numpy as np
from typing import List, Tuple

# ... (COLOR_MAP, get_objects, is_inside_w, transform - from the provided code) ...

def calculate_metrics(input_grid: np.ndarray, output_grid: np.ndarray, expected_grid: np.ndarray) -> dict:
    """Calculates metrics comparing the output and expected grids."""
    correct_pixels = np.sum(output_grid == expected_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    incorrect_pixels = np.where(output_grid != expected_grid)
    incorrect_output_values = output_grid[incorrect_pixels]
    incorrect_expected_values = expected_grid[incorrect_pixels]
    incorrect_details = list(zip(incorrect_pixels[0].tolist(), incorrect_pixels[1].tolist(),
                                 incorrect_output_values.tolist(), incorrect_expected_values.tolist()))

    return {
        "accuracy": accuracy,
        "incorrect_pixels": incorrect_details,
        "input_grid_shape": input_grid.shape,
        "output_grid_shape": output_grid.shape,
        "expected_grid_shape":expected_grid.shape
    }

def run_and_analyze_examples(task_examples: List[Tuple[np.ndarray, np.ndarray]]):
   
    all_metrics = []
    for i, (input_grid, expected_grid) in enumerate(task_examples):
        output_grid = transform(input_grid)
        metrics = calculate_metrics(input_grid, output_grid, expected_grid)
        all_metrics.append(metrics)
    
    return all_metrics

# ARC sample data (replace with your actual data loading)
train_ex = [
    ([[4, 0, 4, 0, 4, 0, 4, 4, 4, 4], [0, 4, 0, 4, 0, 4, 0, 4, 0, 0], [4, 0, 4, 0, 4, 0, 4, 0, 4, 0], [0, 4, 0, 4, 0, 4, 0, 4, 0, 0], [4, 4, 4, 4, 4, 0, 4, 4, 4, 4], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0]], [[4, 3, 4, 3, 4, 3, 4, 4, 4, 4], [3, 4, 3, 4, 3, 4, 3, 4, 3, 3], [4, 3, 4, 3, 4, 3, 4, 3, 4, 3], [3, 4, 3, 4, 3, 4, 3, 4, 3, 3], [4, 4, 4, 4, 4, 3, 4, 4, 4, 4], [3, 3, 3, 3, 3, 2, 3, 3, 3, 3], [3, 3, 3, 3, 3, 2, 3, 3, 3, 3], [3, 3, 3, 3, 3, 2, 3, 3, 3, 3], [3, 3, 3, 3, 3, 2, 3, 3, 3, 3], [3, 3, 3, 3, 3, 2, 3, 3, 3, 3]]),
    ([[4, 0, 4, 0, 4, 4, 4, 4], [0, 4, 0, 4, 0, 0, 0, 0], [4, 0, 4, 0, 4, 0, 4, 4], [0, 4, 0, 4, 0, 4, 0, 0], [4, 4, 4, 4, 4, 0, 4, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0]], [[4, 3, 4, 3, 4, 4, 4, 4], [3, 4, 3, 4, 3, 3, 3, 3], [4, 3, 4, 3, 4, 3, 4, 4], [3, 4, 3, 4, 3, 4, 3, 3], [4, 4, 4, 4, 4, 3, 4, 3], [3, 3, 3, 3, 3, 2, 3, 3], [3, 3, 3, 3, 3, 2, 3, 3], [3, 3, 3, 3, 3, 2, 3, 3]]),
    ([[4, 0, 4, 0, 0, 0, 0, 4, 4, 4], [0, 4, 0, 4, 0, 4, 0, 4, 0, 0], [4, 0, 4, 0, 4, 0, 4, 0, 4, 0], [0, 0, 0, 4, 0, 4, 0, 4, 0, 0], [0, 4, 4, 4, 4, 0, 4, 4, 4, 4], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0, 0]], [[4, 3, 4, 3, 3, 3, 3, 4, 4, 4], [3, 4, 3, 4, 3, 4, 3, 4, 3, 3], [4, 3, 4, 3, 4, 3, 4, 3, 4, 3], [3, 3, 3, 4, 3, 4, 3, 4, 3, 3], [3, 4, 4, 4, 4, 3, 4, 4, 4, 4], [3, 3, 2, 3, 3, 3, 3, 3, 3, 3], [3, 3, 2, 3, 3, 3, 3, 3, 3, 3], [3, 3, 2, 3, 3, 3, 3, 3, 3, 3], [3, 3, 2, 3, 3, 3, 3, 3, 3, 3]]),
    ([[4, 0, 4, 0, 4, 4, 4, 4, 4, 4, 4], [0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0], [4, 0, 4, 0, 4, 0, 4, 4, 4, 4, 4], [0, 4, 0, 4, 0, 4, 0, 4, 0, 0, 0], [4, 4, 4, 4, 4, 0, 4, 0, 4, 0, 4], [0, 0, 0, 0, 0, 3, 0, 4, 0, 4, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0]], [[4, 3, 4, 3, 4, 4, 4, 4, 4, 4, 4], [3, 4, 3, 4, 3, 3, 3, 3, 3, 3, 3], [4, 3, 4, 3, 4, 3, 4, 4, 4, 4, 4], [3, 4, 3, 4, 3, 4, 3, 4, 3, 3, 3], [4, 4, 4, 4, 4, 3, 4, 3, 4, 3, 4], [3, 3, 3, 3, 3, 2, 3, 4, 3, 4, 3], [3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3]]),
    ([[0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0], [4, 0, 0, 4, 4, 0, 0, 4, 4, 4, 0], [4, 0, 0, 4, 4, 0, 0, 4, 4, 0, 4], [0, 4, 4, 0, 0, 4, 4, 0, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0], [3, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0], [0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0]], [[3, 4, 4, 3, 3, 4, 4, 3, 3, 3, 3], [4, 3, 3, 4, 4, 3, 3, 4, 4, 4, 3], [4, 3, 3, 4, 4, 3, 3, 4, 4, 3, 4], [3, 4, 4, 3, 3, 4, 4, 3, 3, 4, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3], [2, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3], [2, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3], [3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]])
]
metrics = run_and_analyze_examples(train_ex)
print (metrics)