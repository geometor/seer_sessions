import numpy as np
# Provided input and expected output grids for example 3
input_grid_3 = [
    [0, 0, 0, 0, 0, 0],
    [0, 5, 0, 7, 0, 0],
    [0, 5, 0, 7, 0, 3],
    [0, 5, 0, 7, 0, 3],
    [0, 5, 0, 7, 0, 3],
    [0, 0, 0, 0, 0, 0],
]

expected_output_3 = [
    [5, 7, 0],
    [5, 7, 0],
    [5, 7, 3],
    [5, 7, 3],
    [5, 7, 3],
    [5, 7, 0],
]

# run through transform
actual_output_3 = transform(input_grid_3)

print(f"Input:\n{np.array(input_grid_3)}")
print(f"Expected Output:\n{np.array(expected_output_3)}")
print(f"Actual Output:\n{np.array(actual_output_3)}")  # Likely incorrect

# Check if Actual Output == Expected Output
print(f"Outputs Match: {np.array_equal(np.array(actual_output_3), np.array(expected_output_3))}")

# Observation
# The relevant columns are the second, fourth and sixth. These
# columns have the first occurences of Gray(5), Orange(7), and
# Green(3) respectively