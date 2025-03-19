import numpy as np

# Example Input/Output Data (from the image, represented as numpy arrays)
train_inputs = [
    np.array([[0, 2, 0], [0, 0, 0], [0, 0, 0]]),
    np.array([[0, 0, 0], [3, 3, 3], [0, 0, 0]]),
    np.array([[0, 0, 0, 0], [0, 0, 4, 4], [0, 0, 4, 4], [0, 0, 0, 0]]),
]

train_outputs = [
    np.array([[0, 2, 0], [0, 2, 0], [0, 2, 0]]),
    np.array([[0, 0, 0], [3, 3, 3], [3, 3, 3]]),
    np.array([[0, 0, 0, 0], [0, 0, 4, 4], [0, 0, 4, 4], [0, 0, 4, 4]]),
]

previous_code_outputs = [
    np.array([[0, 2, 0], [0, 2, 0], [0, 0, 0]]),  # From the provided code
    np.array([[0, 0, 0], [3, 3, 3], [3, 3, 3]]),
    np.array([[0, 0, 0, 0], [0, 0, 4, 4], [0, 0, 4, 4], [0, 0, 4, 4]]),
]

# Analyze each example
for i, (input_grid, expected_output, code_output) in enumerate(zip(train_inputs, train_outputs, previous_code_outputs)):
    print(f"--- Example {i+1} ---")
    print(f"Input:\n{input_grid}")
    print(f"Expected Output:\n{expected_output}")
    print(f"Code Output:\n{code_output}")

    # Compare code output with expected output
    comparison = (expected_output == code_output).all()
    print(f"Match: {comparison}")
    if not comparison:
        diff = np.where(expected_output != code_output)
        print(f"Mismatched indices (row, col): {list(zip(diff[0], diff[1]))}")
