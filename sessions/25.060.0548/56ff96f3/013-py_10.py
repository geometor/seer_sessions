import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    def get_pixel_info(grid, color):
        pixels = np.argwhere(grid == color)
        return len(pixels), pixels.tolist()

    input_green = get_pixel_info(input_grid, 3)
    input_orange = get_pixel_info(input_grid, 7)
    expected_output_green = get_pixel_info(expected_output, 3)
    expected_output_orange = get_pixel_info(expected_output, 7)
    actual_output_green = get_pixel_info(actual_output, 3)
    actual_output_orange = get_pixel_info(actual_output, 7)

    differences = "No differences"
    if not np.array_equal(expected_output, actual_output):
        differences = np.argwhere(expected_output != actual_output).tolist()

    print(f"Input Green: {input_green}")
    print(f"Input Orange: {input_orange}")
    print(f"Expected Output Green: {expected_output_green}")
    print(f"Expected Output Orange: {expected_output_orange}")
    print(f"Actual Output Green: {actual_output_green}")
    print(f"Actual Output Orange: {actual_output_orange}")
    print(f"Differences: {differences}")
    print("-" * 20)

# Provide example data from the training examples.
train_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 3, 3, 0, 0, 0, 7], [0, 0, 0, 0, 3, 3, 0, 0, 0, 7], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 3], [0, 0, 0, 0, 0, 0, 7, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 3]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 0, 0, 0, 0]],
    }
]

def get_transform_result(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    objects = []
    for row_idx, row in enumerate(input_grid):
        for col_idx, pixel in enumerate(row):
            if pixel != 0:
                objects.append((pixel, row_idx, col_idx))

    for color, row, col in objects:
        if color == 3: # green
            for i in range(row, len(output_grid)):
                output_grid[i,col] = 3
                if row + 1 < len(output_grid):
                    output_grid[i,col+1] = 3
        elif color == 7: # orange
            for j in range(col, len(output_grid[row])):
                output_grid[row, j] = 7
    return output_grid.tolist()

for i, ex in enumerate(train_examples):
    print(f"Example: {i}")
    actual_output = get_transform_result(ex["input"])
    analyze_example(ex["input"], ex["output"], actual_output)