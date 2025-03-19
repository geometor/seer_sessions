import numpy as np
input_grid = np.array([[1, 7], [7, 8]])
expected_output_grid = np.array([[7, 8], [1, 7]])
output_grid = np.array([[0., 0., 0., 0., 0., 0., 7., 8., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [7., 0., 0., 0., 0., 0., 0., 0., 0.],
       [8., 7., 0., 0., 0., 0., 0., 0., 0.],
       [1., 0., 0., 0., 0., 0., 0., 0., 0.]])

# compare element by element - count the errors
errors = np.sum(expected_output_grid != output_grid[:2,:2])

print(f"{errors=}")