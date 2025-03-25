"""
Transforms an input grid by first filling colors to the left within each row based on their leftmost occurrence and original order, then filling downwards within each column, and then filling right.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid).tolist()
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each row (Left Fill)
    for r in range(rows):
        #find non-zero colors present in current row, preserve order
        colors = []
        for x in input_grid[r]:
            if x != 0 and x not in colors:
                colors.append(x)

        #iterate through found colors
        for color in colors:
            #find leftmost occurance of colour
            indices = [i for i, x in enumerate(input_grid[r]) if x == color]
            if len(indices)>0:
                leftmost_index = min(indices)
                #fill left
                for i in range(0,leftmost_index):
                    output_grid[r][i] = color

    # Iterate through each column (Down Fill)
    for c in range(cols):
        #find non-zero colors in current column, preserve order
        colors = []
        for r in range(rows):
            if input_grid[r][c] !=0 and input_grid[r][c] not in colors:
                colors.append(input_grid[r][c])

        #Iterate through colors
        for color in colors:
            #find topmost occurance of color
            indices = [r for r in range(rows) if input_grid[r][c] == color]
            if len(indices) > 0:
                topmost_index = min(indices)
                #fill down
                for i in range(topmost_index + 1, rows):
                     if output_grid[i][c] == 0: # only fill if currently 0
                        output_grid[i][c] = color

    # Iterate through each row (Right Fill)
    for r in range(rows):
        #find non-zero colors present in current row, preserve order
        colors = []
        for x in input_grid[r]:
            if x != 0 and x not in colors:
                colors.append(x)
        colors.reverse()
        #iterate through found colors
        for color in colors:
            #find rightmost occurance of colour
            indices = [i for i, x in enumerate(input_grid[r]) if x == color]

            if len(indices)>0:
                rightmost_index = max(indices)
                #fill right
                for i in range(rightmost_index+1,cols):
                    output_grid[r][i] = color

    return output_grid