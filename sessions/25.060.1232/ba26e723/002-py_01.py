"""
The transformation selectively changes yellow to magenta or magenta to yellow in an alternating fashion. The change appears to occur in alternate positions vertically.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for c in range(cols):
        for r in range(rows):
            if output_grid[r,c] == 0:
                continue
            
            if output_grid[r, c] == 4:
                
                changed = False
                if r > 0 and output_grid[r-1,c] == 6:
                    output_grid[r,c] = 6
                    changed = True

                if not changed and c > 0 and output_grid[r, c-1] == 6:
                    output_grid[r, c] = 6
                    changed = True
                
                if not changed and r > 0 and c > 0 and output_grid[r-1,c-1] == 6:
                    output_grid[r,c] = 6
                    changed = True

            elif output_grid[r, c] == 6:
                changed = False

                if r > 0 and output_grid[r-1,c] == 4:
                    output_grid[r,c] = 6 # remain 6
                    changed = True

                if not changed and c > 0 and output_grid[r, c-1] == 4:
                    output_grid[r, c] = 6 # remain 6
                    changed = True
                
                if not changed and r > 0 and c > 0 and output_grid[r-1,c-1] == 4:
                    output_grid[r,c] = 6  # remain 6
                    changed = True


    return output_grid