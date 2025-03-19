import numpy as np

def code_execution(input_grid, expected_output, predicted_output):
    """Executes code and prints results for analysis."""

    print("Input Grid:")
    print(input_grid)
    print("\nExpected Output:")
    print(expected_output)
    print("\nPredicted Output:")
    print(predicted_output)

    input_objects = find_objects(input_grid)
    print("\nIdentified Objects:")
    for obj in input_objects:
        print(f"  Color: {obj['color']}, Pixels: {obj['pixels']}")

    min_row, max_row, min_col, max_col = create_bounding_box(input_objects)
    print(f"\nBounding Box: min_row={min_row}, max_row={max_row}, min_col={min_col}, max_col={max_col}")
    
    if not np.array_equal(expected_output, predicted_output):
        print("\nDifferences between expected and predicted:")
        diff = expected_output != predicted_output
        print(diff)
        print("\nMismatched pixels and their values (Expected, Predicted):")
        
        # Ensure both arrays have the same dimensions for comparison
        min_rows = min(expected_output.shape[0], predicted_output.shape[0])
        min_cols = min(expected_output.shape[1], predicted_output.shape[1])
        
        for row in range(min_rows):
            for col in range(min_cols):
                if expected_output[row, col] != predicted_output[row, col]:
                    print(f"  Row: {row}, Col: {col} - Expected: {expected_output[row, col]}, Predicted: {predicted_output[row, col]}")

        # Handle cases where one array is larger than the other
        if expected_output.shape[0] > predicted_output.shape[0]:
          print("\nAdditional rows in Expected Output:")
          for row in range(predicted_output.shape[0], expected_output.shape[0]):
            print(f"Row {row}: {expected_output[row]}")
        elif expected_output.shape[0] < predicted_output.shape[0]:
           print("\nAdditional rows in Predicted Output:")
           for row in range(expected_output.shape[0], predicted_output.shape[0]):
             print(f"Row {row}: {predicted_output[row]}")
             
        if expected_output.shape[1] > predicted_output.shape[1]:
          print("\nAdditional columns in Expected Output:")
          for col in range(predicted_output.shape[1], expected_output.shape[1]):
            print(f"Col {col}: {expected_output[:,col]}")
        elif expected_output.shape[1] < predicted_output.shape[1]:
            print("\nAdditional columns in Predicted Output:")
            for col in range(expected_output.shape[1], predicted_output.shape[1]):
               print(f"Col {col}: {predicted_output[:,col]}")


# Example data (Replace with actual data from the task)

example_data = [
  (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 6, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
   np.array([[2, 2, 2, 2, 2],
             [2, 0, 0, 0, 2],
             [2, 0, 6, 0, 2],
             [2, 0, 0, 0, 2],
             [2, 2, 2, 2, 2]]),
  'output_1'),
 (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
  np.array([[2, 2, 2],
            [2, 3, 2],
            [2, 2, 2]]),
 'output_2'),
(np.array([[7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7]]),
 np.array([[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
           [2, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]),
  'output_3')
]

for input_grid, expected_output, label in example_data:
  predicted_output = transform(input_grid)
  print(f"\n----- {label} -----")
  code_execution(input_grid, expected_output, predicted_output)