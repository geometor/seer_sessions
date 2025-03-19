import numpy as np

def find_green_pixel(grid):
    """Finds the coordinates of the green pixel in the grid."""
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 3:
                return row_index, col_index
    return None

def transform(input_grid):
    # Determine Output Dimensions
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width

    # Initialize output_grid with all zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Locate Green pixel
    green_row, green_col = find_green_pixel(input_grid)

    # Transform Green to Red at the calculated position
    if green_row is not None:
        output_grid[green_row // 2, green_col] = 2

    return output_grid

def analyze_example(input_grid, expected_output_grid, actual_output_grid):
    report = {
        "input_shape": input_grid.shape,
        "expected_output_shape": expected_output_grid.shape,
        "actual_output_shape": actual_output_grid.shape,
        "input_green_pixel": find_green_pixel(input_grid),
        "output_green_pixel": find_green_pixel(expected_output_grid),
        "correct": np.array_equal(expected_output_grid, actual_output_grid)
    }

    # Compare expected and actual outputs element-wise
    if report["expected_output_shape"] == report["actual_output_shape"]:
      comparison = (expected_output_grid == actual_output_grid)
      report["element_wise_comparison"] = comparison.tolist()
    else:
      report["element_wise_comparison"] = "Shapes do not match"
    
    return report

# Example Usage (replace with actual task data)
task_data = [
    # Example 1
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 3, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 2, 5, 5, 5, 5, 5]])
    },
    # Example 2
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 3, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 2, 5]])
    },
    # Example 3
    {
        "input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                          [5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 5]])
    }

]


reports = []
for example in task_data:
  actual_output = transform(example["input"])
  report = analyze_example(example["input"], example["output"], actual_output)
  reports.append(report)

for i, report in enumerate(reports):
    print(f"--- Example {i+1} ---")
    for key, value in report.items():
        print(f"{key}: {value}")