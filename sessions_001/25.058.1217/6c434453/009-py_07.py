import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    """Calculates pixel-wise accuracy, error count, and identifies error locations."""
    correct_pixels = np.sum(output_grid == predicted_output_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels
    error_count = total_pixels - correct_pixels
    error_locations = np.where(output_grid != predicted_output_grid)
    return accuracy, error_count, error_locations

def analyze_example(example_number, input_grid, output_grid, predicted_output_grid):

    accuracy, error_count, error_locations = calculate_metrics(
        input_grid, output_grid, predicted_output_grid
    )
    print(f"--- Example {example_number} ---")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Error Count: {error_count}")
    print(f"Error Locations (row, col):")
    if error_count >0:
        for r, c in zip(*error_locations):
            print(f"  ({r}, {c}) - Expected: {output_grid[r, c]}, Predicted: {predicted_output_grid[r, c]}")
    else:
        print("  None")

# assuming input_output_pairs are loaded already.
task_data = [
    {
        "input": [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,1,1,1,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],
        "output": [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,2,0,0,0],[0,0,2,2,2,0,0],[0,0,0,2,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
    },
    {
        "input": [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,1,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],
        "output": [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,1,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    },
    {
        "input": [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,1,1,1,0,0,0,0],[0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,1,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
        "output": [[0,0,0,0,0,0,0,0,0],[0,0,2,2,2,0,0,0,0],[0,0,0,2,0,0,0,0,0],[0,0,0,0,0,0,0,2,0],[0,0,0,0,0,0,2,2,2],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    },
    {
        "input": [[1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,1,1,1,0,0,0,0],[0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,1,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,1]],
        "output": [[1,0,0,0,0,0,0,0,0],[0,0,2,2,2,0,0,0,0],[0,0,0,2,0,0,0,0,0],[0,0,0,0,0,0,0,2,0],[0,0,0,0,0,0,2,2,2],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    }
]

from previous_code import transform  # Assuming your previous code is in 'previous_code.py'

for i, example in enumerate(task_data):
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    predicted_output_grid = transform(input_grid)
    analyze_example(i + 1, input_grid, output_grid, predicted_output_grid)