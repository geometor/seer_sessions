import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    objects = find_objects(input_grid)
    center_col = input_grid.shape[1] // 2
    print(f"Input Grid:\n{input_grid}")
    print(f"Expected Output: {expected_output}, Actual Output: {actual_output}")
    print(f"Objects Found: {objects}")
    print(f"Center Column: {center_col}")

    intersected_objects = []
    for obj_color, obj_size, ((min_row, max_row), (min_col, max_col)) in objects:
        if min_col <= center_col <= max_col:
            intersected_objects.append((obj_color, obj_size, ((min_row, max_row), (min_col, max_col))))
    print(f"Intersected Objects: {intersected_objects}")
    print("-" * 20)
    return intersected_objects

# Example Data (replace with actual data from the task)
example_data = [
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
               [8, 8, 0, 0, 0, 0, 0, 8, 8],
               [8, 0, 0, 0, 0, 0, 0, 0, 8],
               [8, 8, 0, 0, 0, 0, 0, 8, 8],
               [8, 8, 8, 8, 8, 8, 8, 8, 8]]), np.array([[4]])),

    (np.array([[8, 8, 8, 8, 8, 8, 8],
               [8, 8, 0, 0, 0, 0, 8],
               [8, 0, 0, 0, 0, 0, 8],
               [8, 0, 0, 0, 0, 0, 8],
               [8, 8, 8, 8, 8, 8, 8]]), np.array([[3]])),

    (np.array([[0, 0, 0, 7, 7, 7, 7, 7, 7],
             [0, 0, 0, 7, 7, 7, 7, 7, 7],
             [0, 0, 0, 7, 7, 7, 7, 7, 7],
             [0, 0, 0, 7, 7, 7, 7, 7, 7],
             [0, 0, 0, 7, 7, 7, 7, 7, 7],
             [0, 0, 0, 7, 7, 7, 7, 7, 7]]), np.array([[9]])),

    (np.array([[7, 7, 7, 7, 0, 0, 0, 0],
              [7, 7, 7, 7, 0, 0, 0, 0],
              [7, 7, 7, 7, 0, 0, 0, 0],
              [7, 7, 7, 7, 0, 0, 0, 0],
              [7, 7, 7, 7, 0, 0, 0, 0],
              [7, 7, 7, 7, 0, 0, 0, 0]]), np.array([[12]])),

    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
               [8, 8, 8, 8, 0, 0, 0, 8, 8],
               [8, 8, 8, 0, 0, 0, 0, 0, 8],
               [8, 8, 0, 0, 0, 0, 0, 8, 8],
               [8, 0, 0, 0, 0, 0, 0, 0, 8]]), np.array([[4]]))
]

# call the function
intersecting_objects = []
for input, output in example_data:
  intersecting_objects.append(analyze_example(input, output, transform(input)))