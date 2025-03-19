import numpy as np
# Assume input_grid and expected_output are defined as numpy arrays.
# input_grid = ...
# expected_output = ...

output_grid = transform(input_grid.copy())
difference = output_grid != expected_output
print(f"Example 2 - Differences:\n{difference}")
print(f"Example 2 - Indices where differences occur: {np.where(difference)}")
print(f"output grid:\n {output_grid}")
print(f"expected output:\n {expected_output}")