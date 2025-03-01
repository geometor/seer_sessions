import numpy as np

def check_output(input_grid, expected_output, transform_func):
    """
    Executes the transform function on the input and compares it to the expected output.

    Args:
        input_grid: The input grid as a NumPy array.
        expected_output: The expected output grid as a NumPy array.
        transform_func: The transformation function to test.

    Returns:
        A tuple: (result, actual_output) where result is True if the actual output matches the expected output,
        and actual_output is the output from the transform_func.
    """
    actual_output = transform_func(input_grid)
    result = np.array_equal(actual_output, expected_output)
    return result, actual_output
train_data = [
    (np.array([
        [5, 5, 5, 5],
        [5, 0, 5, 5],
        [0, 0, 0, 0],
        [5, 0, 5, 5],
        [5, 5, 5, 5],
        [5, 0, 5, 5],
        [5, 0, 5, 5],
        [5, 0, 5, 5],
        [5, 5, 5, 5],
        [5, 0, 5, 5],
        [0, 0, 0, 0],
        [5, 0, 5, 5],
        [5, 5, 5, 5],
        [5, 5, 5, 5]
    ]),
    np.array([
        [0, 2, 0],
        [2, 4, 2],
        [0, 2, 0]
    ])),
   (np.array([
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    ]),
    np.array([
       [0, 0, 0],
       [0, 2, 0],
       [0, 0, 0]
    ])),
    (np.array([
        [5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5],
        [5, 5, 0, 5, 5, 5],
        [5, 5, 0, 5, 5, 5],
        [5, 5, 0, 5, 5, 5],
        [5, 5, 0, 5, 5, 5],
        [5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5]
    ]),
    np.array([
      [0, 0, 0],
      [0, 4, 0],
      [0, 0, 0]
    ])),
    (
    np.array([
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 0, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5]
    ]),
    np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])),
    (np.array([
    [0, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5]
    ]),
    np.array([
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
    ]))
]

results = []
for input_grid, expected_output in train_data:
    result, actual_output = check_output(input_grid, expected_output, transform)
    results.append((input_grid, expected_output, result, actual_output))

for input_grid, expected_output, result, actual_output in results:
    print("Input Grid:")
    print(input_grid)
    print("Expected Output:")
    print(expected_output)
    print("Actual Output:")
    print(actual_output)
    print(f"Match: {result}")
    print("-" * 20)