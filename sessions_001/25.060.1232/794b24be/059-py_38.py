import numpy as np
from typing import List, Tuple

def get_grid_metrics(grid: np.ndarray) -> dict:
    """Computes and returns metrics for a given grid."""
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    return {
        "dimensions": grid.shape,
        "color_counts": color_counts,
    }

def analyze_example(input_grid: np.ndarray, output_grid: np.ndarray, predicted_grid:np.ndarray) -> dict:
    """Analyzes a single input-output example."""
    return {
        "input": get_grid_metrics(input_grid),
        "output": get_grid_metrics(output_grid),
        "predicted": get_grid_metrics(predicted_grid),
        "correct" : np.array_equal(output_grid, predicted_grid)
    }
def transform(input_grid):
    # Initialize output grid with the same dimensions and all zeros,
    # then copy the input grid to preserve non-blue pixels.
    output_grid = np.copy(input_grid)

    # Iterate through all pixels in the input grid
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            # If a pixel is blue (1) in the input, change it to red (2) in the output
            if pixel_value == 1:
                output_grid[row_index, col_index] = 2

    return output_grid

def show_grid(grid, title):
  print(title)
  for row in grid:
    print(row)

# Example data (replace with your actual data)
example_data: List[Tuple[np.ndarray, np.ndarray]] = [
  (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 1, 1, 1, 0],
            [0, 5, 5, 5, 0, 1, 1, 1, 0],
            [0, 5, 5, 5, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 2, 2, 2, 0],
            [0, 5, 5, 5, 0, 2, 2, 2, 0],
            [0, 5, 5, 5, 0, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]])),

  (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 5, 5, 5, 0, 1, 1, 1, 0],
            [0, 5, 5, 5, 0, 5, 5, 5, 0, 1, 1, 1, 0],
            [0, 5, 5, 5, 0, 5, 5, 5, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 5, 5, 5, 0, 2, 2, 2, 0],
            [0, 5, 5, 5, 0, 5, 5, 5, 0, 2, 2, 2, 0],
            [0, 5, 5, 5, 0, 5, 5, 5, 0, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])),

  (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0, 1, 1, 1, 1, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0, 1, 1, 1, 1, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0, 2, 2, 2, 2, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0, 2, 2, 2, 2, 0],
            [0, 5, 5, 5, 5, 5, 5, 5, 0, 2, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])),
]

analysis_results = [analyze_example(in_grid, out_grid, transform(in_grid)) for in_grid, out_grid in example_data]

for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Input:    {result['input']}")
    print(f"  Output:   {result['output']}")
    print(f"  Predict:  {result['predicted']}")
    print(f"  Correct:  {result['correct']}")