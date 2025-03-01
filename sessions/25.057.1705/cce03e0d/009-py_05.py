import numpy as np
input_grid = np.array([[0, 5, 0], [5, 5, 5], [0, 5, 0]])
expected_output_grid = np.array([[5, 0, 5], [0, 0, 0], [5, 0, 5]])
output_grid = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 5.],
       [0., 0., 0., 0., 0., 0., 5., 5., 5.],
       [0., 0., 0., 0., 0., 0., 0., 5., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 5., 0., 0., 0., 0., 0., 0., 0.],
       [5., 5., 5., 0., 0., 0., 0., 0., 0.],
       [0., 5., 0., 0., 0., 0., 0., 0., 0.]])

# compare element by element - count the errors
errors = np.sum(expected_output_grid != output_grid[:3,:3])

print(f"{errors=}")