import numpy as np

# Provided training outputs (replace with actual data from the prompt)
outputs = [
    np.array([[2, 2, 2], [4, 4, 4], [2, 2, 2]]),
    np.array([[2, 2, 2], [4, 4, 4], [2, 2, 2]]),
    np.array([[2, 2, 2], [4, 4, 4], [2, 2, 2]]),
    np.array([[2, 2, 2], [4, 4, 4], [2, 2, 2]]),
    np.array([[2, 2, 2], [4, 4, 4], [2, 2, 2]]),
]

# Check if all outputs are identical
all_same = all(np.array_equal(outputs[0], output) for output in outputs)
print(f"All outputs are identical: {all_same}")

# print the shape and content of the first output
print(outputs[0].shape)
print(outputs[0])
