import numpy as np

def get_horizontal_lines(grid):
    """
    Identifies horizontal lines of non-zero, same-colored pixels.
    Returns a list of tuples: (row_index, start_col, end_col, color).
    """
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = -1
        current_color = 0
        for c in range(cols):
            if grid[r, c] != 0:
                if start_col == -1:
                    start_col = c
                    current_color = grid[r, c]
                elif grid[r, c] != current_color:
                    lines.append((r, start_col, c - 1, current_color))
                    start_col = c
                    current_color = grid[r, c]
            elif start_col != -1:
                lines.append((r, start_col, c - 1, current_color))
                start_col = -1
                current_color = 0
        if start_col != -1:
             lines.append((r, start_col, cols-1, current_color))
    return lines

def analyze_transform(input_grid, expected_output_grid):
    """
    Transforms the input grid and prints intermediate values for analysis.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    print("Input Grid:")
    print(input_grid_np)


    # Get horizontal lines
    lines = get_horizontal_lines(input_grid_np)
    print("\nDetected Horizontal Lines:")
    for line in lines:
        print(line)


    print("\nTransformation Process:")
    # Determine new row index based on original row's distance to bottom
    for line in lines:
        row_index, start_col, end_col, color = line
        new_row_index = rows - 1 - row_index
        print(f"Line: {line}, Original Row Index: {row_index}, New Row Index (calculated as rows - 1 - row_index): {new_row_index}")

        output_grid[new_row_index, start_col:end_col+1] = color

    print("\nPredicted Output Grid:")
    print(output_grid)
    print("\nExpected Output Grid")
    print(np.array(expected_output_grid))

    print("\nDifferences")
    diff = output_grid == np.array(expected_output_grid)
    print(diff)

    return output_grid.tolist()


task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 7, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 0, 0, 0], [0, 0, 7, 7, 7, 7, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0], [0, 3, 3, 3, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2]],
        },
    ],
    "test": [{"input": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 9, 0, 0], [0, 0, 0, 0, 0], [1, 1, 0, 0, 0]], "output": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 9, 0, 0], [1, 1, 0, 0, 0]]}],
}

for example in task["train"]:
      analyze_transform(example["input"], example["output"])