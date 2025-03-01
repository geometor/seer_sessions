import numpy as np

def find_gray_center(grid):
    """Finds the coordinates of the gray pixel (color 5) in the grid."""
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == 5:
                return (row_idx, col_idx)
    return None

def get_moved_pixels(input_grid, output_grid):
    """Identifies pixels that have different positions between input and output."""
    moved_pixels = []
    for row_idx in range(input_grid.shape[0]):
        for col_idx in range(input_grid.shape[1]):
            if input_grid[row_idx, col_idx] != output_grid[row_idx, col_idx]:
                moved_pixels.append(((row_idx, col_idx), input_grid[row_idx, col_idx]))
    return moved_pixels

task_data = [
    {
        "input": np.array([[8, 1, 1, 1, 8, 1, 1, 1, 8],
                           [1, 8, 1, 1, 1, 1, 1, 8, 1],
                           [1, 1, 8, 1, 5, 1, 8, 1, 1],
                           [1, 1, 1, 8, 1, 8, 1, 1, 1],
                           [8, 1, 1, 1, 8, 1, 1, 1, 8]]),
        "output": np.array([[8, 1, 1, 1, 8, 1, 1, 1, 8],
                            [1, 8, 1, 1, 1, 1, 1, 8, 1],
                            [1, 1, 8, 8, 5, 8, 8, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [8, 1, 1, 1, 8, 1, 1, 1, 8]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 2, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 6, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[7, 0, 0, 0, 0, 0, 0, 0, 7],
                           [0, 7, 0, 0, 0, 0, 0, 7, 0],
                           [0, 0, 7, 0, 0, 0, 7, 0, 0],
                           [0, 0, 0, 7, 5, 7, 0, 0, 0],
                           [0, 0, 0, 0, 7, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[7, 0, 0, 0, 0, 0, 0, 0, 7],
                            [0, 7, 0, 0, 0, 0, 0, 7, 0],
                            [0, 0, 7, 0, 0, 0, 7, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0],
                            [0, 0, 0, 7, 7, 7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }

]

for i, example in enumerate(task_data):
    input_grid = example['input']
    output_grid = example['output']
    center = find_gray_center(input_grid)
    moved_pixels = get_moved_pixels(input_grid, output_grid)
    print(f"Example {i+1}:")
    print(f"  Gray Center: {center}")
    print(f"  Moved Pixels: {moved_pixels}")

    # check prediction against actual output
    predicted_output = transform(input_grid)
    if np.array_equal(output_grid, predicted_output):
      print("  Prediction: Correct")
    else:
      print("  Prediction: Incorrect")
      print("Expected")
      print(output_grid)
      print("Actual")
      print(predicted_output)