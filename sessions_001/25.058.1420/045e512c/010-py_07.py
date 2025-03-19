"""
This program transforms an input grid containing a cross-shaped object into an output grid where the cross is inflated and mirrored.

1.  **Identify the "cross" object:** Locate the cross-shaped object in the input grid, defined by connected pixels of colors 1, 2, and 4. Note its center coordinates and the colors of each arm.
2.  **Inflate the Cross Center:** The central blue (1) pixel expands into a 3x3 block of blue (1) pixels, in the same center location.
3.  **Inflate and Recolor Yellow:** The two yellow (4) pixels in the shape:
    *   Expand to a vertical and horizontal 3x1 yellow (4) block, respectively
    *   A 3x3 yellow (4) block is placed around the center of the shape.
4.  **Mirror the Red:** The single red (2) pixels is replicated to create a 3x3 square, plus four 3x1 bars.
5.  **Preserve Background:** All other pixels in the grid remain white (0).

"""

import numpy as np

def find_cross_center(grid):
    # Find the center of the cross shape (blue pixel)
    rows, cols = np.where(grid == 1)
    if len(rows) > 0:
        return (int(np.mean(rows)), int(np.mean(cols)))
    return None

def get_cross_arms(grid, center):
     # Get coordinates of the cross arms
    arms = {}
    
    #Check for red (2)
    if grid[center[0],center[1]-2] == 2:
        arms['left'] = (center[0], center[1]-2)
        
    if grid[center[0],center[1]+2] == 4:
        arms['right'] = (center[0], center[1]+2)
        
    if grid[center[0]-3,center[1]] == 4:
        arms['top'] = (center[0]-3, center[1])
        
    if grid[center[0]+1,center[1]] == 1:
        arms['bottom'] = (center[0]+1, center[1])

    return arms

def transform(input_grid):
    # Initialize output_grid with the same dimensions and background color
    output_grid = np.zeros_like(input_grid)

    # Find the cross center
    center = find_cross_center(input_grid)

    if center is None:
        return output_grid # Return empty grid if no cross is found

    arms = get_cross_arms(input_grid, center)

    # Inflate the center (blue)
    for i in range(center[0] - 1, center[0] + 2):
        for j in range(center[1] - 1, center[1] + 2):
            if 0 <= i < output_grid.shape[0] and 0 <= j < output_grid.shape[1]:
              output_grid[i, j] = 1

    # Inflate and recolor yellow parts
    
    if 'top' in arms:
        for i in range(arms['top'][0]-1, arms['top'][0] + 2):
            if 0 <= i < output_grid.shape[0]:
                output_grid[i, arms['top'][1]] = 4

    if 'right' in arms:
        for j in range(arms['right'][1], arms['right'][1] + 3):
            if 0 <= j < output_grid.shape[1]:
               output_grid[arms['right'][0], j] = 4

    # mirror and create yellow structure
    for i in range(center[0] - 2, center[0] + 3):
        for j in range(center[1] - 2, center[1] + 3):
            if abs(i - center[0]) <=1  and abs(j-center[1]) <=1:
                continue
            
            if (abs(i - center[0]) == 2  or abs(j - center[1]) == 2) and (0 <= i < output_grid.shape[0] and 0 <= j < output_grid.shape[1]) :
                output_grid[i,j]=4
            

    # Mirror red
    if 'left' in arms:

        for i in range(arms['left'][0] - 1, arms['left'][0] + 2):
            for j in range(arms['left'][1] - 2, arms['left'][1] + 1):
                if 0 <= i < output_grid.shape[0] and 0 <= j < output_grid.shape[1]:
                  output_grid[i, j] = 2

    # add additional red bars
    for i in range(center[0]-1, center[0]+2):
        output_grid[i, center[1]-4] = 2

    return output_grid