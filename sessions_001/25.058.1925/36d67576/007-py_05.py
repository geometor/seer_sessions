import numpy as np
input_grid = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,3,0,1,0],
                       [0,0,0,0,0,0,0,0,0,0,0,1,0],
                       [0,0,0,0,0,0,0,0,0,0,4,1,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,4,0,0,0],
                       [4,4,4,4,4,4,4,4,4,4,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0]])
output_grid = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,4,0,4,0],
                        [0,0,0,0,0,0,0,0,0,0,0,1,0],
                        [0,0,0,0,0,0,0,0,0,0,1,1,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,3,0,0,0],
                        [4,4,4,4,4,4,4,4,4,4,3,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0]])
code_execution(input_grid, output_grid)