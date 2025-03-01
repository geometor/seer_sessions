import numpy as np

def find_red_square(grid):
    # Find the top-left corner coordinates of the red square
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 2 and grid[r+1, c] == 2 and grid[r, c+1] == 2 and grid[r+1, c+1] == 2:
                return (r, c)  # Return top-left corner
    return None

def find_gray_pixels(grid):
    # Find coordinates of all gray pixels
    return np.argwhere(grid == 5)

def calculate_accuracy(predicted_output, expected_output):
     return np.all(predicted_output == expected_output)
    
def report(task_name, input_grid, predicted_output, expected_output):
    
    print(f"task name: {task_name}")
    print(f"{input_grid=}")
    print(f"{predicted_output=}")
    print(f"{expected_output=}")
    
    red_square = find_red_square(input_grid)
    gray_pixels = find_gray_pixels(input_grid)    
    
    print(f"{red_square=}")
    print(f"{gray_pixels=}")

    print(f"accuracy = {calculate_accuracy(predicted_output, expected_output)}")    
    print("---")

examples = [
    ("example 1",
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 5, 8, 8, 8, 8, 8, 5, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 5, 8, 8, 8, 8, 8, 5, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 0, 8, 8, 8, 8, 8, 0, 8],
                  [8, 5, 8, 8, 8, 8, 8, 5, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 0, 8, 8, 8, 8, 8, 0, 8],
                  [8, 5, 8, 8, 8, 8, 8, 5, 8]]),
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 5, 8],
                  [8, 5, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 5, 8],
                  [8, 5, 8, 8, 8, 8, 8, 8, 8]])
    ),
       ("example 2",
       np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                 [8, 8, 8, 8, 8, 8, 8, 8, 8],
                 [8, 8, 5, 8, 8, 8, 5, 8, 8],
                 [8, 8, 8, 8, 8, 8, 8, 8, 8],
                 [8, 8, 8, 8, 8, 8, 8, 8, 8],
                 [8, 8, 8, 8, 2, 2, 8, 8, 8],
                 [8, 8, 8, 8, 2, 2, 8, 8, 8],
                 [8, 8, 8, 8, 8, 8, 8, 8, 8],
                 [8, 8, 5, 8, 8, 8, 5, 8, 8]]),
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 0, 8, 8, 8, 0, 8, 8],
                  [8, 8, 5, 8, 8, 8, 5, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 5, 8, 8, 8, 5, 8, 8]]),
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 5, 8, 8],
                  [8, 8, 5, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 2, 2, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 5, 8, 8, 8, 5, 8, 8]])
    ),
    ("example 3",
         np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 5, 8, 8, 8, 8, 8, 5, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 5, 8, 8, 8, 8, 8, 5, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 5, 8, 8, 8, 8, 8, 5, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 5, 8, 8, 8, 8, 8, 5, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 0, 8, 8, 8, 8, 8, 0, 8],
                  [8, 5, 8, 8, 8, 8, 8, 5, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 0, 8, 8, 8, 8, 8, 0, 8],
                  [8, 5, 8, 8, 8, 8, 8, 5, 8]]))

]

from SEER_code_exec import code_execution

for task_name, input_grid, predicted_output, expected_output in examples:
    result = code_execution(
        f"report('{task_name}', input_grid, transform(input_grid), expected_output)"
    )
