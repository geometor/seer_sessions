import numpy as np

def show_grid(grid, title="Grid"):
    print(f"\n--- {title} ---")
    if grid.size == 0:  # Check for empty array
        print("Empty Grid")
    else:
        print(grid)

def compare_grids(grid1, grid2):
    """Compares two grids and returns a boolean if equal and difference if not"""
    are_equal = np.array_equal(grid1, grid2)
    if are_equal:
      return True, None
    else:
      return False, grid1 - grid2

def analyze_example(input_grid, expected_output, actual_output):
    """Analyzes a single example."""

    print("\n----- Example Analysis -----")
    show_grid(input_grid, "Input Grid")
    show_grid(expected_output, "Expected Output")
    show_grid(actual_output, "Actual Output")

    grids_equal, diff = compare_grids(expected_output,actual_output)
    print(f"\nExpected Output == Actual Output: {grids_equal}")
    if not grids_equal:
      show_grid(diff,"Difference")
    

# Example Data (Replace with actual data from the task)

example_data = [
  (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 6, 6, 6, 6]]),
np.array([[6, 6, 6, 6]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 0, 0, 0],
       [0, 0, 5, 5, 5, 5, 5, 0, 0],
       [0, 0, 5, 5, 5, 5, 5, 0, 0],
       [0, 0, 0, 5, 5, 5, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 6]]),
np.array([[6]])),
  (np.array([[6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 5, 5, 5, 5, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
 np.array([[6]]))
]
task_id = "e177c588"
#Get the transform function from the code
for i, (input_grid, expected_output) in enumerate(example_data):
    actual_output = transform(input_grid)
    analyze_example(input_grid, expected_output, actual_output)
    print(f"transform success: {np.array_equal(expected_output,actual_output)}")
