# Hypothetical Code for Metrics Collection (Illustrative)
import numpy as np

def find_vertical_lines(grid, color):
    """Finds vertical lines of a specified color in a grid."""
    lines = []
    rows, cols = grid.shape
    for j in range(cols):
        start = -1
        for i in range(rows):
            if grid[i, j] == color:
                if start == -1:
                    start = i
            elif start != -1:
                lines.append((start, i - 1, j))
                start = -1
        if start != -1:
            lines.append((start, rows - 1, j))
    return lines

def transform(input_grid):
    """Transforms the input grid by replacing blue lines with green lines."""
    output_grid = input_grid.copy()
    blue_lines = find_vertical_lines(input_grid, 1)  # Find blue lines
    for start_row, end_row, col in blue_lines:
        output_grid[start_row:end_row+1, col] = 3  # Replace with green
    return output_grid

def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    correct = np.array_equal(output_grid, predicted_output_grid)
    input_lines = find_vertical_lines(input_grid, 1)  # Blue lines
    predicted_lines = find_vertical_lines(predicted_output_grid, 3) # Green Lines
    output_lines = find_vertical_lines(output_grid, 3)
    return {
        "correct": correct,
        "input_blue_lines": input_lines,
        "output_green_lines": output_lines,
        "predicted_green_lines": predicted_lines
    }


task_data =  [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 3, 0, 0, 0],
                            [0, 0, 0, 3, 0, 0, 0],
                            [0, 0, 0, 3, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [3, 0, 0, 0, 0, 0],
                            [3, 0, 0, 0, 0, 0],
                            [3, 0, 0, 0, 0, 0],
                            [3, 0, 0, 0, 0, 0]])
    },
        {
        "input": np.array([[0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0]]),
        "output": np.array([[0, 0, 3, 0, 0],
                            [0, 0, 3, 0, 0],
                            [0, 0, 3, 0, 0],
                            [0, 0, 3, 0, 0],
                            [0, 0, 3, 0, 0]])
    },
    {
       "input": np.array( [[0, 1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 3, 0, 0, 0, 0, 0],
                            [0, 3, 0, 0, 0, 0, 0],
                            [0, 3, 0, 0, 0, 0, 0],
                            [0, 3, 0, 0, 0, 0, 0],
                            [0, 3, 0, 0, 0, 0, 0]])
    }
]

results = []
for example in task_data:
  predicted_output = transform(example["input"])
  metrics = calculate_metrics(example["input"], example["output"], predicted_output)
  results.append(metrics)

print(results)