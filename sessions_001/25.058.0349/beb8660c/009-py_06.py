import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a report."""
    grid1 = np.array(grid1)
    grid2 = np.array(grid2)
    if grid1.shape != grid2.shape:
        return "Different Shapes"

    diff = grid1 != grid2
    if not np.any(diff):
        return "Identical"

    num_diffs = np.sum(diff)
    diff_positions = np.argwhere(diff)

    report = {
      "num_diffs": int(num_diffs),
      "diff_positions": diff_positions.tolist()
    }

    return report

def find_rows_with_objects(grid):
   grid = np.array(grid)
   rows_with_objects = []
   for i, row in enumerate(grid):
       if np.any(row != 0):  # Check if the row has any non-background pixels
          rows_with_objects.append(i)
   return rows_with_objects

def print_example_info(task, transform_function):
  """Prints an analysis of each training example"""
  for i, example in enumerate(task["train"]):
      input_grid = example["input"]
      expected_output_grid = example["output"]
      actual_output_grid = transform_function(input_grid)
      comparison = compare_grids(actual_output_grid, expected_output_grid)
      print(f"--- Example {i+1} ---")
      print(f"Input Rows with Objects: {find_rows_with_objects(input_grid)}")
      print(f"Expected Output Rows with Objects: {find_rows_with_objects(expected_output_grid)}")

      if comparison == "Identical":
        print("Result: PASS")
      else:
        print("Result: FAIL")
        print(f"Comparison details: {comparison}")
        print(f"Actual output: {actual_output_grid}")
        print(f"Expected output: {expected_output_grid}")

      print()

# Example Usage (replace with actual task data)
task = {
    "train": [
        {
            "input": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            "output": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0], [0, 0, 0], [0, 2, 2], [0, 2, 2]],
            "output": [[0, 0, 0], [0, 0, 0], [0, 2, 2], [0, 2, 2]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]],
            "output": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]],
        },
         {
            "input": [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 1]],
            "output": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1]],
        },
    ]
}

print_example_info(task, transform)

