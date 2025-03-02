import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    input_objects = find_objects(input_grid)
    expected_objects = find_objects(expected_output)

    input_colors = set(input_grid.flatten())
    expected_colors = set(expected_output.flatten()) if expected_output.size > 0 else set()
    
    input_verticals = [obj for obj in input_objects if is_vertical_line(obj,input_grid)]

    print(f"  Input Colors: {input_colors}")
    print(f"  Expected Colors: {expected_colors}")
    print(f"  Input Vertical Lines Found: {len(input_verticals) > 0}")
    print(f"  Expected Output Shape: {expected_output.shape}")
    print(f"  Actual Output Shape: {actual_output.shape}")
    if actual_output.size > 0:
        print(f"  Actual Output color: {set(actual_output.flatten())}")
    print(f"  Correct: {np.array_equal(actual_output, expected_output)}")

# Example Grids (replace with your actual data)
examples = [
    (np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 1, 0]]),
     np.array([[1],
              [1],
              [1]])),
      (np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 0, 0],
              [0, 0, 0, 4, 0, 0],
              [0, 0, 0, 4, 0, 0],
              [0, 0, 0, 4, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
      np.array([[4],
              [4],
              [4],
              [4]])),
      (np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 7, 7, 7, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
      np.array([[0,0,0,0,0,0]]).reshape(0,)),
      (np.array([[0, 0, 0, 0, 0, 0],
              [0, 7, 0, 0, 0, 0],
              [0, 7, 0, 0, 0, 0],
              [0, 7, 0, 0, 0, 0],
              [0, 7, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
      np.array([[7],
              [7],
              [7],
              [7]])),
]

for i, (input_grid, expected_output) in enumerate(examples):
    actual_output = transform(input_grid)
    print(f"Example {i + 1}:")
    analyze_example(input_grid, expected_output, actual_output)