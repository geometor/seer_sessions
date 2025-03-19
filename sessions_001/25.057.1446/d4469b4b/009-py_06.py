import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    report = {}

    report["input_dims"] = input_grid.shape
    report["expected_output_dims"] = expected_output.shape
    report["actual_output_dims"] = actual_output.shape

    #input_grid analysis
    report["input_color_counts"] = {color: np.sum(input_grid == color) for color in range(10)}
    input_bb = get_bounding_box(input_grid, 1)
    report["input_bounding_box"] = input_bb if input_bb else "None"

    #expected_output analysis
    report["expected_output_color_counts"] = {color: np.sum(expected_output == color) for color in range(10)}
    expected_bb = get_bounding_box(expected_output, 1)
    report["expected_output_bounding_box"] = expected_bb if expected_bb else "None"

    #actual_output analysis
    report["actual_output_color_counts"] = {color: np.sum(actual_output == color) for color in range(10)}
    actual_bb = get_bounding_box(actual_output, 1)
    report["actual_output_bounding_box"] = actual_bb if actual_bb else "None"

    # Pixel-by-pixel comparison (only if dimensions match)
    if expected_output.shape == actual_output.shape:
        comparison = (expected_output == actual_output)
        report["pixel_comparison"] = comparison.tolist()
        report["mismatches"] = np.sum(~comparison)
    else:
        report["pixel_comparison"] = "Dimensions mismatch"
        report["mismatches"] = "N/A"

    return report


def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)


def transform(input_grid):
    # Find bounding box of blue pixels (color 1)
    bounding_box = get_bounding_box(input_grid, 1)
    if bounding_box is None:
        return np.zeros((1, 1), dtype=int)  # Handle cases where the color doesn't exist

    min_row, max_row, min_col, max_col = bounding_box

    # Create output grid based on bounding box dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Map input pixels within the bounding box to the output grid
    for i in range(output_height):
        for j in range(output_width):
            input_row = min_row + i
            input_col = min_col + j
            if input_grid[input_row, input_col] == 1:
                output_grid[i, j] = 5
            else:
                output_grid[i, j] = 0

    return output_grid

# Example Usage (assuming you have your input/output pairs)
task_examples = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0],
               [0, 5, 0],
               [0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0],
               [0, 5, 0],
               [0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0],
               [0, 5, 0],
               [0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0],
               [0, 5, 0],
               [0, 0, 0]])
     )
]

reports = []
for input_grid, expected_output in task_examples:
    actual_output = transform(input_grid)
    report = analyze_example(input_grid, expected_output, actual_output)
    reports.append(report)

for i, report in enumerate(reports):
    print(f"--- Example {i+1} ---")
    for key, value in report.items():
        print(f"{key}: {value}")