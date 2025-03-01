import numpy as np

def transform(input_grid):
    """Transforms the input grid by extending yellow and red colors downwards until a black pixel or the bottom is reached."""
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input_grid
    rows, cols = output_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Iterate through each row in the column
        for i in range(rows):
            # Extend yellow color downwards
            if input_grid[i, j] == 4:  # Check for yellow pixel
                for k in range(i + 1, rows):  # Iterate downwards from current position
                    if output_grid[k, j] == 1: # Check for black pixel
                        break  # Stop extending if black pixel is encountered
                    output_grid[k, j] = 4  # Set the pixel to yellow

            # Extend red color downwards
            elif input_grid[i, j] == 2:  # Check for red pixel
                for k in range(i + 1, rows): # Iterate downwards from current position
                    if output_grid[k,j] == 1:  #check for black pixel
                        break  # Stop extending if black pixel is encountered.
                    output_grid[k, j] = 2  # Set the pixel to red

    return output_grid

# Define the task examples.  I will combine all training examples into one dictionary
task_examples = {
  "train_0": {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 0, 0, 0, 4, 4, 4], [0, 0, 0, 0, 0, 0, 4, 4, 4, 4], [0, 0, 0, 0, 0, 4, 4, 4, 4, 4], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 0, 0, 0, 4, 4, 4], [0, 0, 0, 0, 0, 0, 4, 4, 4, 4], [0, 0, 0, 0, 0, 4, 4, 4, 4, 4], [0, 0, 0, 0, 4, 4, 4, 4, 4, 4]],
    },
    "train_1": {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, 1, 1, 2, 0], [0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, 1, 1, 2, 0], [0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
    },
    "train_2": {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 2, 2, 2, 2]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 2, 2, 2, 2]],
    },
    "train_3": {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 4, 4, 0], [0, 0, 0, 0, 4, 4, 4, 0], [0, 0, 0, 4, 4, 4, 4, 0], [0, 0, 0, 4, 4, 4, 4, 1], [0, 0, 0, 0, 4, 4, 4, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 4, 4, 0], [0, 0, 0, 0, 4, 4, 4, 0], [0, 0, 0, 4, 4, 4, 4, 0], [0, 0, 0, 4, 4, 4, 4, 1], [0, 0, 0, 0, 4, 4, 4, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
    },
}

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid highlighting the differences."""
    return np.where(grid1 == grid2, 0, 1)

for example_name, example_data in task_examples.items():
  input_grid = np.array(example_data["input"])
  expected_output = np.array(example_data["output"])
  actual_output = transform(input_grid)
  diff_grid = compare_grids(expected_output,actual_output)

  print(f"--- {example_name} ---")
  print("Input:\n", input_grid)
  print("Expected Output:\n", expected_output)
  print("Actual Output:\n", actual_output)
  print("Differences (1 indicates a difference):\n", diff_grid)
  print("\n")