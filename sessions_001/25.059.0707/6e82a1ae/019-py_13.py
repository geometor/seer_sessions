import numpy as np

def code_execution(input_grid, expected_output, transform_func):
    """Executes the transform function and compares the result with the expected output."""
    actual_output = transform_func(input_grid)
    comparison = np.array_equal(actual_output, expected_output)
    return actual_output, comparison

# Example usage (replace with actual data from your examples):
# Assuming 'transform' is your transformation function
# and you have 'train' which is your list of training dictionaries
# like this:
# train = [
#     {'input': np.array(...), 'output': np.array(...)},
#     {'input': np.array(...), 'output': np.array(...)},
#     ...
# ]

# Example 1 (assuming this is your first training example)
train = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 5, 5, 5, 0, 0, 0],
            [0, 5, 5, 5, 0, 5, 0],
            [0, 0, 0, 0, 0, 5, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 0, 3, 0],
            [0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ])
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
    },
        {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 5, 0, 0],
            [0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 5, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 5, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 3, 0, 0],
            [0, 0, 1, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 1, 0, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
    }
]
actual_output_1, comparison_1 = code_execution(train[0]['input'], train[0]['output'], transform)
print(f"Example 1 Comparison: {comparison_1}")
print(f"Actual Output 1:\n{actual_output_1}")

actual_output_2, comparison_2 = code_execution(train[1]['input'], train[1]['output'], transform)
print(f"Example 2 Comparison: {comparison_2}")
print(f"Actual Output 2:\n{actual_output_2}")

actual_output_3, comparison_3 = code_execution(train[2]['input'], train[2]['output'], transform)
print(f"Example 3 Comparison: {comparison_3}")
print(f"Actual Output 3:\n{actual_output_3}")