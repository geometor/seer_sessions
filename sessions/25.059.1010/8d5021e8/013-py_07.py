import numpy as np

def measure_grid(grid):
    """Calculates grid dimensions and unique color counts."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    return rows, cols, unique_colors, color_counts

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):
    """Analyzes an example and returns metrics."""
    input_rows, input_cols, input_colors, input_counts = measure_grid(input_grid)
    expected_rows, expected_cols, expected_colors, expected_counts = measure_grid(expected_output_grid)
    predicted_rows, predicted_cols, predicted_colors, predicted_counts = measure_grid(predicted_output_grid)

    analysis = {
        "input": {
            "rows": input_rows,
            "cols": input_cols,
            "unique_colors": input_colors.tolist(),
            "color_counts": input_counts,
        },
        "expected_output": {
            "rows": expected_rows,
            "cols": expected_cols,
            "unique_colors": expected_colors.tolist(),
            "color_counts": expected_counts,
        },
        "predicted_output": {
            "rows": predicted_rows,
            "cols": predicted_cols,
            "unique_colors": predicted_colors.tolist(),
            "color_counts": predicted_counts,
        }
    }
    return analysis

# Example Usage (assuming grids are defined)
# Assuming task variable is created and grids are made available as demonstrated
# in previous responses.

train_analyses = []

for i in range(len(task['train'])):
    input_grid = np.array(task['train'][i]['input'])
    expected_output_grid = np.array(task['train'][i]['output'])
    predicted_output_grid = transform(input_grid) # use previous code
    analysis = analyze_example(input_grid, expected_output_grid, predicted_output_grid)
    train_analyses.append(analysis)

print (train_analyses)