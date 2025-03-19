"""
1.  **Identify Relevant Colors:** Locate all pixels in the input grid that are colored blue (1), red (2), or yellow (4).
2.  **Determine Output Region:** Find the smallest bounding box that contains the four uppermost and leftmost of the pixels identified in step 1. If there are fewer than four such pixels, include empty cells to make a total of 4. The indices of those pixels become the indices of the cells in the output that should be colored green.
3.  **Create Output Grid:** Create a 4x4 output grid filled with white (0).
4. **Populate the Output Grid**: Iterate through the positions from step 2. If a given position contains a relevant color, change the corresponding cell in the 4x4 output grid to be green(3).
5.  **Output:** The final output is a 4x4 grid.
"""

import numpy as np

def find_relevant_pixels(input_grid):
    """Finds the positions of blue (1), red (2), and yellow (4) pixels."""
    input_array = np.array(input_grid)
    relevant_pixels = []
    for i in range(input_array.shape[0]):
        for j in range(input_array.shape[1]):
            if input_array[i, j] in (1, 2, 4):
                relevant_pixels.append((i, j))
    return relevant_pixels

def determine_output_region(relevant_pixels):
    """Determines the 4x4 output region based on relevant pixel positions."""
    
    if not relevant_pixels:
      return [(i,j) for i in range(4) for j in range(4)]

    rows = sorted(list(set([r for r,c in relevant_pixels])))
    cols = sorted(list(set([c for r,c in relevant_pixels])))

    #ensure we have at least 4 rows
    while len(rows) < 4:
      rows.append(rows[-1]+1)

    #ensure we have at least 4 cols
    while len(cols) < 4:
      cols.append(cols[-1]+1)

    output_region_coords = []

    #select at most the first four of each
    for row in rows[:4]:
        for col in cols[:4]:
            output_region_coords.append((row,col))

    return output_region_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Find positions of relevant colors (blue, red, yellow)
    relevant_pixels = find_relevant_pixels(input_grid)

    # Determine the coordinates that correspond to output
    output_region_coords = determine_output_region(relevant_pixels)

    #print(relevant_pixels)
    #print(output_region_coords)

    # Populate output grid
    for i in range(4):
      for j in range(4):
        if (output_region_coords[i*4 + j][0] < np.array(input_grid).shape[0] and
            output_region_coords[i*4 + j][1] < np.array(input_grid).shape[1] and
            input_grid[output_region_coords[i*4 + j][0]][output_region_coords[i*4+j][1]] in (1,2,4)):
          output_grid[i][j] = 3
    return output_grid.tolist()