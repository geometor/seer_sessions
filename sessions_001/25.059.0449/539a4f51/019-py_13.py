def analyze_example(example_number, task, code):
    input_grid = task['train'][example_number]['input']
    expected_output_grid = task['train'][example_number]['output']
    actual_output_grid = code(input_grid)

    print(f"--- Example {example_number + 1} ---")
    print(f"Input Dimensions: {np.array(input_grid).shape}")
    print(f"Input Colors: {np.unique(input_grid)}")
    print(f"Expected Output Dimensions: {np.array(expected_output_grid).shape}")
    print(f"Expected Output Colors: {np.unique(expected_output_grid)}")
    print(f"Actual Output Dimensions: {np.array(actual_output_grid).shape}")
    print(f"Actual Output Colors: {np.unique(actual_output_grid)}")

    if np.array_equal(expected_output_grid, actual_output_grid):
        print("Output: Correct")
    else:
        print("Output: Incorrect")
        print("Differences (Expected - Actual):")
        # simple diff - not a pixel by pixel comparison, just shape and unique values
        expected_arr = np.array(expected_output_grid)
        actual_arr = np.array(actual_output_grid)
        if expected_arr.shape != actual_arr.shape:
          print("shapes are different")
        else:
           diff = expected_arr - actual_arr
           print(np.unique(diff))

# load ARC task and previous code (transform function)
import json
import numpy as np

#correct function, but misses the pattern cycling
def transform(input_grid):
    # Create a copy of the input grid.
    input_grid = np.array(input_grid)
    duplicated_grid = np.copy(input_grid)

    # Combine the original and duplicated grids horizontally.
    output_grid = np.concatenate((input_grid, duplicated_grid), axis=1)

    # Get the number of rows and columns in the combined grid
    num_rows, num_cols = output_grid.shape
    
    # Get original input_grid size
    in_rows, in_cols = input_grid.shape

    # Append rows
    new_rows = []
    for i in range(in_rows):
      row = []
      for j in range(in_cols):
        row.append(input_grid[i,j])
      for j in range(in_cols):
        row.append(input_grid[i,j])
      new_rows.append(row)

    new_rows = np.array(new_rows)

    output_grid = np.concatenate((output_grid, new_rows), axis=0)

    return output_grid.tolist()

with open('1b60fb0c.json', 'r') as f:
  task = json.load(f)

for i in range(len(task['train'])):
    analyze_example(i, task, transform)
