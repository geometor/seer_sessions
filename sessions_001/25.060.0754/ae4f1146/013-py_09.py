import numpy as np

def analyze_subgrid_errors(input_grid, expected_output_grid, predicted_output_grid):
    """
    Analyzes subgrids where the predicted output differs from the expected output.
    Prints information about these subgrids, including the subgrid itself, the expected output,
    and the predicted output. Also counts color frequency
    """
    input_array = np.array(input_grid)
    expected_array = np.array(expected_output_grid)
    predicted_array = np.array(predicted_output_grid)

    errors = []

    for i in range(3):
        for j in range(3):
            if expected_array[i, j] != predicted_array[i, j]:
                subgrid = input_array[i*3:(i+1)*3, j*3:(j+1)*3]
                print(f"Error in subgrid ({i}, {j}):")
                print("Subgrid:")
                print(subgrid)
                print("Expected Output:", expected_array[i, j])
                print("Predicted Output:", predicted_array[i, j])

                # Count color frequencies within the subgrid
                unique_colors, counts = np.unique(subgrid, return_counts=True)
                color_counts = dict(zip(unique_colors, counts))
                print("Color Counts:", color_counts)
                errors.append((i,j))

    return errors

# Example Usage (replace with actual data from the task):
examples = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
  ], [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
  ], [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
  ], [
    [0, 0, 0],
    [0, 2, 0],
    [0, 0, 0]
  ], [
    [0, 0, 0],
    [0, 2, 0],
    [0, 0, 0]
  ]),
   ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4, 4, 0, 0, 0],
    [0, 0, 0, 4, 4, 4, 0, 0, 0],
    [0, 0, 0, 4, 4, 4, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
  ], [
   [0, 0, 0],
   [0, 4, 0],
   [0, 0, 0]
  ], [
    [0, 0, 0],
    [0, 4, 0],
    [0, 0, 0]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 5, 5, 0, 0, 0],
    [0, 0, 0, 5, 5, 5, 0, 0, 0],
    [0, 0, 0, 5, 5, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 6, 6, 6]
  ], [
    [0, 0, 0],
    [0, 5, 0],
    [0, 0, 6]
  ], [
    [0, 0, 0],
    [0, 5, 0],
    [0, 0, 6]
  ]),
 ([
    [7, 7, 7, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 0, 0, 0, 0, 0, 0],
    [7, 7, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 9, 9, 9],
    [0, 0, 0, 0, 0, 0, 9, 9, 9],
    [0, 0, 0, 0, 0, 0, 9, 9, 9]
  ], [
   [7, 0, 0],
   [0, 8, 0],
   [0, 0, 9]
  ], [
    [7, 0, 0],
    [0, 8, 0],
    [0, 0, 9]
  ])
]

for i, (input_grid, expected_output_grid, predicted_output_grid) in enumerate(examples):
    errors = analyze_subgrid_errors(input_grid, expected_output_grid, predicted_output_grid)
    print(f'{len(errors)} errors in example {i}')
