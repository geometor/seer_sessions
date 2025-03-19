def analyze_results(examples, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):

        # set up input and output grids
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)
        actual_output = transform_function(input_grid)

        # check for equal shape and then all values equal
        shape_match = actual_output.shape == expected_output.shape
        values_match = np.array_equal(actual_output, expected_output)

        # store the result
        results.append({
            "example": i + 1,
            "shape_match": shape_match,
            "values_match": values_match,
            "input_shape": input_grid.shape,
            "output_shape": actual_output.shape,
            "expected_shape": expected_output.shape,
      })

    for result in results:
        print(f"Example: {result['example']}")
        print(f"  Shape Match: {result['shape_match']}")
        print(f"  Values Match: {result['values_match']}")
        print(f"  Input Shape: {result['input_shape']}")
        print(f"  Output Shape: {result['output_shape']}")
        print(f"  Expected Shape: {result['expected_shape']}")
        print("-" * 20)

    return results

# Example Usage - dummy data, replace later
examples = [
([[0, 0, 0],
  [0, 1, 0],
  [0, 0, 0]],
 [[1, 0, 1],
  [1, 1, 1],
  [1, 0, 1]]),

([[0, 1, 0, 1, 0],
  [1, 0, 1, 0, 1],
  [0, 1, 0, 1, 0],
  [1, 0, 1, 0, 1]],
 [[1, 0, 1, 0, 1],
  [0, 1, 0, 1, 0],
  [1, 0, 1, 0, 1],
  [0, 1, 0, 1, 0]]),

([[0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0]],
[[1, 1, 1, 1, 1],
 [1, 1, 0, 1, 1],
 [1, 0, 1, 0, 1],
 [1, 1, 0, 1, 1],
 [1, 1, 1, 1, 1]])
]

analyze_results(examples, transform)
