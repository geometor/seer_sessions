import numpy as np
from typing import Tuple, List

def find_azure_pixels(grid: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Finds the coordinates of azure pixels (value 8) in a grid."""
    return np.where(grid == 8)

def are_diagonal(azure_coords: Tuple[np.ndarray, np.ndarray]) -> bool:
    """Checks if two azure pixels are diagonally positioned."""
    if len(azure_coords[0]) < 2:
      return False
    return azure_coords[0][0] != azure_coords[0][1] and azure_coords[1][0] != azure_coords[1][1]

def analyze_example(input_grid: np.ndarray, expected_output_grid: np.ndarray, observed_output_grid: np.ndarray) -> dict:
    """Analyzes a single example and returns relevant metrics."""
    input_azure_coords = find_azure_pixels(input_grid)
    expected_output_azure_coords = find_azure_pixels(expected_output_grid)
    observed_output_azure_coords = find_azure_pixels(observed_output_grid)
    
    analysis = {
        'input_dims': input_grid.shape,
        'input_azure_coords': input_azure_coords,
        'expected_output_dims': expected_output_grid.shape,
        'expected_output_azure_coords': expected_output_azure_coords,
        'observed_output_dims': observed_output_grid.shape,
        'observed_output_azure_coords': observed_output_azure_coords,
        'input_azure_diagonal': are_diagonal(input_azure_coords),
    }
    return analysis

def compare(expected_output_grid, observed_output_grid):
    if expected_output_grid.shape != observed_output_grid.shape:
        return False
    return np.array_equal(expected_output_grid, observed_output_grid)

def report(task, transform):
    results = []
    correct_count = 0
    for i, example in enumerate(task['train']):
        inp = np.array(example['input'])
        exp = np.array(example['output'])
        obs = transform(inp)
        this_result = {
            'example_index': i,
            'correct': compare(exp, obs),
            'analysis': analyze_example(inp, exp, obs)
        }
        results.append(this_result)

    for r in results:
      print(f"Example Index: {r['example_index']}, Correct: {r['correct']}")
      print(f"  Input Dims: {r['analysis']['input_dims']}, Azure Coords: {r['analysis']['input_azure_coords']}")
      print(f"  Expected Output Dims: {r['analysis']['expected_output_dims']}, Azure Coords: {r['analysis']['expected_output_azure_coords']}")
      print(f"  Observed Output Dims: {r['analysis']['observed_output_dims']}, Azure Coords: {r['analysis']['observed_output_azure_coords']}")
      print(f"  Input Azure Diagonal: {r['analysis']['input_azure_diagonal']}")
    return results

# previous transform function

def transform(input_grid):
    # Find azure pixels in the input grid.
    azure_coords = find_azure_pixels(input_grid)
    
    # Determine if azure pixels are diagonal.
    diagonal = are_diagonal(azure_coords)

    if diagonal:
        # Calculate output dimensions for diagonal case.
        max_row = max(azure_coords[0])
        max_col = max(azure_coords[1])
        output_height = max_row + 4
        output_width = max_col + 7
        output_grid = np.zeros((output_height, output_width), dtype=int)

        # Place two azure pixels at opposite corners.
        output_grid[max_row,max_col+6] = 8
        output_grid[max_row+3,0] = 8

    else:
        # Calculate output dimensions for non-diagonal case.
        output_height = 4
        output_width = input_grid.shape[1] + 3 if input_grid.shape[1] > input_grid.shape[0] else  input_grid.shape[0] + 6
        output_grid = np.zeros((output_height, output_width), dtype=int)

        # Place four azure pixels at the extreme corners.
        output_grid[0, 0] = 8
        output_grid[0, -1] = 8
        output_grid[-1, 0] = 8
        output_grid[-1, -1] = 8

    return output_grid