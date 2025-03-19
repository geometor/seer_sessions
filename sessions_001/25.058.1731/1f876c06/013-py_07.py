import numpy as np
from typing import List, Tuple

def analyze_transform(input_grid: np.ndarray, output_grid: np.ndarray, predicted_grid: np.ndarray) -> List[Tuple[int, int, int, int, int, bool, bool]]:
    """
    Analyzes the transformation of each non-zero pixel in the input grid.

    Args:
        input_grid: The original input grid.
        output_grid: The expected output grid.
        predicted_grid: The output grid predicted by the transform function.

    Returns:
        A list of tuples, where each tuple contains:
        - original row index
        - original column index
        - pixel value
        - new row index (expected)
        - new column index (expected)
        - correctness of row prediction (predicted_grid vs. output_grid)
        - correctness of column prediction (predicted_grid vs. output_grid)
            If a pixel disappears, the new row/col indices are set to -1, and correctness is False.
    """
    analysis = []
    input_pixels = get_nonzero_pixels(input_grid)

    for r, c, val in input_pixels:
        shift = val
        if c >= r:
            new_r_expected = r + shift
            new_c_expected = c - shift
        else:
          new_r_expected = r + shift
          new_c_expected = c + shift

        # Check if the expected position is out of bounds
        if not (0 <= new_r_expected < output_grid.shape[0] and 0 <= new_c_expected < output_grid.shape[1]):
            new_r_expected = -1
            new_c_expected = -1
            row_correct = predicted_grid[r,c] == 0 # should not have any output
            col_correct = predicted_grid[r,c] == 0 # should not have any output
        else:          
          row_correct = predicted_grid[new_r_expected, new_c_expected] == output_grid[new_r_expected, new_c_expected]
          col_correct = predicted_grid[new_r_expected, new_c_expected] == output_grid[new_r_expected, new_c_expected]

        analysis.append((r, c, val, new_r_expected, new_c_expected, row_correct, col_correct))

    return analysis

def create_report(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_grid = transform(input_grid.copy())  # Use a copy to avoid modifying the original

        analysis = analyze_transform(input_grid, output_grid, predicted_grid)

        print(f"  Example {i+1}:")
        for r, c, val, new_r, new_c, row_correct, col_correct in analysis:
            if new_r == -1:
                print(f"    Pixel ({r}, {c}, {val}) disappears. Correct: {(row_correct and col_correct)}")
            else:
                print(f"    Pixel ({r}, {c}, {val}) -> ({new_r}, {new_c}). Row Correct: {row_correct}, Col Correct: {col_correct}")
        print(f"    Predicted Output:\n{predicted_grid}")
        print(f"    Expected Output:\n{output_grid}")
        print("-" * 20)

# Mock task and data for demonstration
task = {
    "name": "Example Task",
        "train": [
            {
                "input": [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0]],
                "output": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]
            },
            {
                "input": [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 2, 0], [0, 0, 0, 0]],
                "output": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]
            },
            {
                "input" : [[0, 0, 5, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                "output": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
            }

        ]
    }

create_report(task)
