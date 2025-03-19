import numpy as np

def analyze_results(input_grid, expected_output, actual_output):
    """Analyzes the differences between the expected and actual outputs."""

    differences = (expected_output != actual_output)
    diff_coords = np.argwhere(differences)

    orange_pixels_expected = np.argwhere(expected_output == 7)
    orange_pixels_actual = np.argwhere(actual_output == 7)

    print(f"Number of differing pixels: {len(diff_coords)}")
    print(f"Number of orange pixels (expected): {len(orange_pixels_expected)}")
    print(f"Number of orange pixels (actual): {len(orange_pixels_actual)}")
    #check for any blue that is not blue in output
    blue_pixels_input = np.argwhere(input_grid == 1)
    blue_changed = 0
    for bp in blue_pixels_input:
      if actual_output[bp[0],bp[1]] != 1:
        blue_changed += 1
    print(f"Number of blue pixels changed: {blue_changed}")

    # Check for adjacent differences: pixels where *either* expected OR actual output have orange, but not both
    adjacent_differences = 0
    for row in range(expected_output.shape[0]):
      for col in range(expected_output.shape[1]):
        if expected_output[row,col] == 7 or actual_output[row,col] == 7:
          #now check neighbors
          for r,c in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr = row + r
            nc = col + c
            if 0 <= nr < expected_output.shape[0] and 0 <= nc < expected_output.shape[1]:
              if (expected_output[nr,nc] == 7 and actual_output[nr,nc] != 7) or \
                (expected_output[nr,nc] != 7 and actual_output[nr,nc] == 7):
                adjacent_differences += 1

    print(f"Adjacent Difference count {adjacent_differences}")

task_data = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "expected": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "actual": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "expected": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 1, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "actual": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]])

    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "expected": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                              [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "actual": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                            [0, 7, 0, 0, 0, 0, 0, 0, 0, 0]])

    }
]

for i, data in enumerate(task_data):
  print(f"Example {i+1}:")
  analyze_results(data["input"], data["expected"], data["actual"])
  print("-" * 20)