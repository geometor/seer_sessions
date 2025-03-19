import numpy as np

# Provided input and expected output grids for example 2
input_grid_2 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 4, 0, 2],
    [1, 0, 4, 0, 2],
    [1, 0, 4, 0, 2],
    [1, 0, 4, 0, 2],
]
expected_output_2 = [
    [1, 4, 2],
    [1, 4, 2],
    [1, 4, 2],
    [1, 4, 2],
    [1, 4, 2],
]

# run through transform
actual_output_2 = transform(input_grid_2)

print(f"Input:\n{np.array(input_grid_2)}")
print(f"Expected Output:\n{np.array(expected_output_2)}")
print(f"Actual Output:\n{np.array(actual_output_2)}")

# Check if Actual Output == Expected Output
print(f"Outputs Match: {np.array_equal(np.array(actual_output_2), np.array(expected_output_2))}")

# Observation
# The relevant columns are the first, third and fifth. These
# columns have the first occurences of Blue(1), Yellow(4), and
# Red(2) respectively