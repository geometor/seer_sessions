import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """
    Analyzes the differences between the expected output and the predicted output.
    """
    results = {}

    # Check if gray lines are preserved
    results["gray_preserved"] = np.all(
        (input_grid == 5) == (predicted_grid == 5)
    )

    # Blue pixel analysis (Correct, Incorrectly Removed, Incorrectly Kept)
    blue_pixels_expected = (output_grid == 1)
    blue_pixels_predicted = (predicted_grid == 1)
    correct_blue_pixels = np.sum(blue_pixels_expected & blue_pixels_predicted)
    incorrectly_removed_blue = np.sum(blue_pixels_expected & ~blue_pixels_predicted)
    incorrectly_kept_blue = np.sum(~blue_pixels_expected & blue_pixels_predicted)

    results["correct_blue"] = correct_blue_pixels
    results["incorrect_removed_blue"] = incorrectly_removed_blue
    results["incorrect_kept_blue"] = incorrectly_kept_blue

    # Analyze 3x3 square
    if np.any(blue_pixels_predicted):
        # Basic Check - does the count of blue match 9?
        blue_count = np.count_nonzero(predicted_grid == 1)
        results["blue_square_pixels"] = blue_count

    return results

def get_bottom_gray_line(grid):
    rows, cols = grid.shape
    for r in reversed(range(rows)):
        for c in range(cols):
            if grid[r, c] == 5:
                return r, c # Just return the first cell in the bottom gray line
    return None, None

def get_grid_string(grid):
  return str(grid).replace(' ', ',')

# Loop through the examples and apply the analysis:
task_data = [
  {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 5, 1, 5]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 5, 5, 5]]
  },
  {
    "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 5, 1, 1, 5], [0, 0, 0, 0, 0, 0, 5, 1, 1, 5], [0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
    "input" : [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0], [1, 1, 1, 5, 0, 0, 0, 0, 0, 0], [1, 1, 5, 5, 0, 0, 0, 0, 0, 0], [1, 5, 1, 1, 0, 0, 0, 0, 0, 0], [5, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output" : [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0]]
    }
]

results_summary = []
for i, example in enumerate(task_data):
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])

    # get existing transform result
    predicted_grid = transform(input_grid)
    metrics = analyze_example(input_grid, output_grid, predicted_grid)
    metrics['example_index'] = (i + 1)
    # Get position of the bottom-most gray
    bottom_row, bottom_col = get_bottom_gray_line(input_grid)
    metrics['bottom_gray_row'] = bottom_row
    metrics['bottom_gray_col'] = bottom_col

    metrics['input_grid'] = get_grid_string(input_grid)
    metrics['output_grid'] = get_grid_string(output_grid)
    metrics['predicted_grid'] = get_grid_string(predicted_grid)

    results_summary.append(metrics)

print(results_summary)