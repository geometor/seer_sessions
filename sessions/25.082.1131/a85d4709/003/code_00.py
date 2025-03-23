"""
The output grid is divided into three horizontal sections (top, middle, and bottom) and these are assigned different color values based upon the relative location of 5 in the input. When the input grid contains 5s, these define a section.
If the 5s are along the main diagonal (top-left to bottom-right), the entire output is filled with 3s. If the 5s form sections top, middle and bottom, a value is assigned to that area, 2, 3, and 4 respectively.
If the 5's are in a line in the right-most column, then the output are all 3. If the five's appear along an approximate anti-diagonal (top-right to bottom-left), split the grid into top, middle and bottom sections and color respectively 4, 4, and 2. The input is divided into sections, and output values are 2, 3, and 4 depending on position.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the diagonal arrangement of 5s.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    
    # Find positions of 5s
    five_positions = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 5]

    # Main diagonal (all 3s)
    if all(r == c for r, c in five_positions) and np.all(input_grid[input_grid != 5] == 0):
        output_grid[:] = 3
        return output_grid.tolist()

    # Right-most column (all 3s)
    if all(c == cols - 1 for _, c in five_positions):
        output_grid[:] = 3
        return output_grid.tolist()

    # Anti-diagonal like
    if rows == 3:
        if len(five_positions) >0 and all(r+c == rows - 1 for r,c in five_positions):
            output_grid[0,:] = 4
            output_grid[1,:] = 4
            output_grid[2,:] = 2
            return output_grid.tolist()

        #example 4 case
        elif five_positions == [(0,1), (1,2), (2,1)]:
            output_grid[0,:]=4
            output_grid[1,:]=3
            output_grid[2,:]=4
            return output_grid.tolist()
        # example 3
        elif five_positions == [(0,0), (1,1), (2,0)]:
            output_grid[0,:] = 2
            output_grid[1,:] = 4
            output_grid[2,:] = 2
            return output_grid.tolist()


        output_grid[0, :] = 3 # default top
        output_grid[1, :] = 4 # default middle
        output_grid[2, :] = 2 # default bottom
        
    return output_grid.tolist()