import numpy as np

def code_execution(input_grid, expected_output, transform_func):
    """Executes the transform function and compares the output to the expected output."""
    actual_output = transform_func(input_grid)
    comparison = np.array_equal(actual_output, expected_output)
    return actual_output, comparison

# Example Data (replace with your actual data)
examples = [
    (
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 2, 0, 2, 0]])
    ),
     (
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 2, 0, 0, 2, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]])
    ),
    (
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 2, 0, 0, 2, 0],
                  [0, 0, 0, 0, 0, 0]])
    ),
     (
        np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 2, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 2, 0, 0, 0, 0, 0]])
    ),
    (
        np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 2, 0, 0, 0, 2, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]])
    )
]

results = []
for input_grid, expected_output in examples:
    actual_output, comparison = code_execution(input_grid, expected_output, transform)
    results.append((input_grid, expected_output, actual_output, comparison))

for i, (input_grid, expected_output, actual_output, comparison) in enumerate(results):
    print(f"Example {i + 1}:")
    print(f"Input:\n{input_grid}")
    print(f"Expected Output:\n{expected_output}")
    print(f"Actual Output:\n{actual_output}")
    print(f"Comparison (Correct): {comparison}\n")
