import numpy as np

def find_special_row(grid):
    # Iterate through rows to find the one with all other values as zero
    for i, row in enumerate(grid):
        is_special = True
        for j, pixel in enumerate(row):
          if j%2 == 1 and pixel != 0:
            is_special = False
        if is_special:
            return i
    return -1  # Return -1 if no such row is found

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find special row
    special_row_index = find_special_row(input_grid)
    # print(special_row_index)

    if special_row_index != -1:
      # get special row
      special_row = input_grid[special_row_index]

      # replace output grid row pixels
      for i in range(len(special_row)):
        if special_row[i] != 0:
          output_grid[special_row_index] = np.full(len(special_row), special_row[i])


    return output_grid

def check_grids(task):
    correct_count = 0
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid.copy())

        special_row_index = find_special_row(input_grid)
        print(f"Example: {example}")
        print(f"  Special Row Index (predicted): {special_row_index}")

        if special_row_index != -1:
            print(f" values on special row: {input_grid[special_row_index]}")

        if np.array_equal(predicted_output, output_grid):
            correct_count += 1
            print("  Correct Prediction")
        else:
            print("  Incorrect Prediction")
            print(f"  Predicted Output:\n{predicted_output}")
            print(f"  Expected Output:\n{output_grid}")
        print("-" * 20)
    print(f"Correct Predictions: {correct_count} / {len(task['train'])}")

# Example usage (replace with the actual task data):
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 3, 0, 4, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 7, 0, 8, 0, 5, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7], [0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 5, 0, 1, 0, 9, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [5, 5, 5, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0], [0, 2, 0, 2, 0], [0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0], [2, 2, 2, 2, 2], [0, 0, 0, 0, 0]],
        },
    ]
}

check_grids(task)