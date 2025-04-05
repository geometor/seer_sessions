import numpy as np

# Example input (simulating the type)
input_data_train_1 = np.array([5, 0, 8, 0, 3, 0, 0, 0, 3, 4, 0, 0])
expected_output_train_1 = np.array([5, 8, 8, 3, 3, 3, 3, 3, 3, 4, 0, 0]) # Assuming output should also be array for logic check

# Basic properties
print(f"Input type: {type(input_data_train_1)}")
print(f"Input shape: {input_data_train_1.shape}")
print(f"Input dtype: {input_data_train_1.dtype}")

# Find non-zero indices
non_zero_indices = np.nonzero(input_data_train_1)[0]
print(f"Non-zero indices: {non_zero_indices}")

# Expected number of segments to process (pairs of non-zero indices)
num_segments = len(non_zero_indices) - 1 if len(non_zero_indices) >= 2 else 0
print(f"Number of segments between non-zeros: {num_segments}")

# Check if the expected output length matches input length
output_length_match = len(input_data_train_1) == len(expected_output_train_1)
print(f"Input/Output length match: {output_length_match}")
