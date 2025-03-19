import numpy as np

def code_execution(input_grid, output_grid, predicted_output):
    """
    Analyze the input, expected output, and predicted output grids.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)

    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(output_grid)
    print("Predicted Output Grid:")
    print(predicted_output)

    # calculate error
    diff = output_grid - predicted_output
    print("Difference")
    print(diff)

    # find objects
    blue_red_input_obj = find_objects(input_grid, [1,2])
    yellow_input_obj = find_objects(input_grid, [4])

    blue_red_output_obj = find_objects(output_grid, [1,2])
    yellow_output_obj = find_objects(output_grid, [4])

    print("Input Blue/Red Objects")
    print(blue_red_input_obj)
    print("Input Yellow Objects")
    print(yellow_input_obj)
    print("Output Blue/Red Objects")
    print(blue_red_output_obj)
    print("Output Yellow Objects")
    print(yellow_output_obj)

    # Check for object property consistencies (e.g., size, adjacency)
    # Check if objects are present in both input and output

# provided examples
train_ex = [
    [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 4, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 8, 0, 0, 0], [3, 3, 3, 0, 0, 0, 8, 0, 0, 0], [3, 3, 3, 0, 0, 0, 8, 0, 0, 0]], [[0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 2, 2, 2, 0], [0, 0, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0]]],
    [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 2, 0], [0, 0, 4, 0]]],
    [[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 2, 1, 0], [0, 0, 0, 0, 0, 0, 2, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 1, 1, 0], [0, 2, 1, 0], [0, 2, 4, 0], [0, 0, 0, 0]]],
    [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0], [0, 2, 2, 1, 0, 0], [0, 2, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]],
    [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 2, 1, 0], [0, 0, 0, 0, 0, 0, 0, 2, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 1, 0], [0, 2, 1, 0], [0, 2, 4, 0], [0, 0, 0, 0]]]
]

# execute analysis for each example
for ex in train_ex:
  input_grid, output_grid = ex
  predicted_output = transform(input_grid)
  code_execution(input_grid, output_grid, predicted_output)
  print("-" * 80)
