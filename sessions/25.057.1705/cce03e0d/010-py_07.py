import numpy as np

# Example 1 (as provided)
input_grid1 = np.array([[0, 5, 0], [5, 5, 5], [0, 5, 0]])
expected_output_grid1 = np.array([[5, 0, 5], [0, 0, 0], [5, 0, 5]])
output_grid1 = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 5.],
       [0., 0., 0., 0., 0., 0., 5., 5., 5.],
       [0., 0., 0., 0., 0., 0., 0., 5., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 5., 0., 0., 0., 0., 0., 0., 0.],
       [5., 5., 5., 0., 0., 0., 0., 0., 0.],
       [0., 5., 0., 0., 0., 0., 0., 0., 0.]])
errors1 = np.sum(expected_output_grid1 != output_grid1[:3,:3])
print(f"Example 1 Errors: {errors1}")

# Example 2 (Hypothetical - let's assume a different example)
input_grid2 = np.array([[5,0,5],[0,5,0],[5,0,5]])
expected_output_grid2 = np.array([[0,5,0],[5,0,5],[0,5,0]])
output_grid2 = transform(input_grid2) # we do not have transform defined, but that's ok
errors2 = np.sum(expected_output_grid2 != output_grid2[:3,:3]) # assuming transform gives 9x9
print(f"Example 2 Errors (hypothetical transform): {errors2}")

# Example 3 (Another hypothetical example)
input_grid3 = np.array([[5,5,5],[5,0,5],[5,5,5]])
expected_output_grid3 = np.array([[0,0,0],[0,5,0],[0,0,0]])
output_grid3 = transform(input_grid3)
errors3 = np.sum(expected_output_grid3 != output_grid3[:3, :3])
print(f"Example 3 Errors (hypothetical): {errors3}")
