"""
1.  **Expand the Grid:** Create a new grid that is three times the width and three times the height of the original grid, plus one extra column.
2.  **Fill with Zeros:** Initially, fill the entire expanded grid with zeros (white).
3.  **Replicate Input Colors:** Tile the input grid three times across and three times down in the expanded grid.
4.  **Add Red Column:** Add a column of red (2) pixels at the rightmost edge of the expanded grid. The height of the red column is determined by three times the height of the *input* grid. The red column starts on the first row.

"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 3, input_width * 3 + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Tile input grid
    for i in range(3):
        for j in range(3):
            output_grid[i*input_height:(i+1)*input_height, j*input_width:(j+1)*input_width] = input_grid

    # Add red column
    output_grid[:input_height*3, -1] = 2
    
    return output_grid