import numpy as np

def calculate_metrics(input_grid, output_grid, expected_output_grid):
    """Calculates differences between the generated output and expected output."""
    correct_pixels = np.sum(output_grid == expected_output_grid)
    incorrect_pixels = np.sum(output_grid != expected_output_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    color_changes = {}
    for color in np.unique(input_grid):
        indices = np.where(input_grid == color)
        new_colors = output_grid[indices]
        if len(new_colors) > 0:
          color_changes[color] = np.unique(new_colors).tolist() # unique list

    return {
        "correct_pixels": int(correct_pixels),
        "incorrect_pixels": int(incorrect_pixels),
        "total_pixels": int(total_pixels),
        "accuracy": float(accuracy),
        "color_changes": color_changes,
    }

# define example grids from web page - training pairs from task 1
input_grids = [
    np.array([[4, 9, 9], [9, 4, 9], [4, 9, 9]]),
    np.array([[0, 9, 2], [9, 9, 9], [0, 9, 9]]),
    np.array([[9, 9, 4], [9, 4, 9], [4, 4, 4]]),
    np.array([[4, 9, 2], [9, 4, 0], [4, 0, 9]]),
]

expected_output_grids = [
    np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
    np.array([[0, 5, 0], [5, 5, 5], [0, 5, 5]]),
    np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
    np.array([[5, 5, 0], [5, 5, 0], [5, 0, 5]]),
]

results = []
for i, (input_grid, expected_output_grid) in enumerate(zip(input_grids, expected_output_grids)):
    output_grid = transform(input_grid)
    metrics = calculate_metrics(input_grid, output_grid, expected_output_grid)
    results.append(
        {
            "example_index": i,
             "metrics": metrics
        }
    )

for item in results:
  print(item)