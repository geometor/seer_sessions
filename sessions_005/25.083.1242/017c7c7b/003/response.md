```python
"""
Iterate through each cell of the input grid. If the cell's value is 0 (white),
keep it as 0 (white) in the output grid. If the cell's value is 1 (blue),
change it to 2 (red) in the output grid. 
Count the number of blue pixels in the input grid. 
Copy the last row of partially created output grid and append it. 
Append it 'n' times, where 'n' is the number of blue pixels divided by input row length.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1]), dtype=int)

    # change output pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 1:
                output_grid[r, c] = 2
            else:
                output_grid[r,c] = input_grid[r,c]
    
    #count blue pixels
    n_blue = np.sum(input_grid == 1)

    #calculate number of rows to append
    n_appended = n_blue // input_grid.shape[1]

    #resize output grid
    new_shape = (output_grid.shape[0] + n_appended, output_grid.shape[1])
    output_grid.resize(new_shape, refcheck=False)

    #copy last row to a new one and append
    for i in range(n_appended):
        output_grid[input_grid.shape[0] + i, :] = output_grid[input_grid.shape[0]-1, :]


    return output_grid.tolist()
```