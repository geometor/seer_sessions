import numpy as np
from typing import List, Dict, Tuple, Set

def calculate_metrics(inputs: List[List[List[int]]], outputs: List[List[List[int]]]) -> List[Dict]:
    """Calculates metrics for input-output pairs."""
    metrics_list = []
    for input_grid, output_grid in zip(inputs, outputs):
        input_np = np.array(input_grid)
        output_np = np.array(output_grid)

        # Find the bounding box for colors 1 and 8.
        min_row, max_row, min_col, max_col = find_bounding_box(input_np)
        bounding_box_height = max_row - min_row + 1
        bounding_box_width = max_col - min_col + 1

        metrics = {
            'input_dims': input_np.shape,
            'output_dims': output_np.shape,
            'unique_colors_input': set(np.unique(input_np)),
            'unique_colors_output': set(np.unique(output_np)),
            'bounding_box_dims': (bounding_box_height, bounding_box_width),
            'result_dims': np.array(transform(input_grid)).shape,
        }
        metrics_list.append(metrics)
    return metrics_list
def find_bounding_box(grid):
    """Finds the bounding box of pixels with color 1 or 8."""
    rows, cols = np.where((grid == 1) | (grid == 8))
    if rows.size > 0:  # Check if any 1s or 8s were found
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)
        return min_row, max_row, min_col, max_col
    else:
        return 0, 0, 0, 0  # Return a default (0,0) to (0,0) bounding box if no 1s or 8s

def extract_subgrid(grid, min_row, max_row, min_col, max_col):
    """Extracts the subgrid defined by the bounding box."""
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_np = np.array(input_grid)

    # Find the bounding box for colors 1 and 8.
    min_row, max_row, min_col, max_col = find_bounding_box(input_np)

    # Extract the subgrid.
    output_grid = extract_subgrid(input_np, min_row, max_row, min_col, max_col)

    return output_grid.tolist()

def pretty_print_metrics(metrics_list: List[Dict], train_success: List[bool]) -> None:
    """Pretty prints the metrics."""
    for i, metrics in enumerate(metrics_list):
        print(f"Example {i+1}:")
        print(f"  Input Dimensions: {metrics['input_dims']}")
        print(f"  Output Dimensions: {metrics['output_dims']}")
        print(f"  Unique Colors in Input: {metrics['unique_colors_input']}")
        print(f"  Unique Colors in Output: {metrics['unique_colors_output']}")
        print(f"  Bounding Box Dimensions: {metrics['bounding_box_dims']}")
        print(f"  Result Dimensions: {metrics['result_dims']}")
        print(f"  Correct: {train_success[i]}")
        print("-" * 20)

# get the metrics
# train_inputs and train_outputs are provided in the context
metrics_list = calculate_metrics(train_inputs, train_outputs)
pretty_print_metrics(metrics_list, train_success)