"""
1.  **Identify Columns of Interest:** Examine each column in the input grid. A column is a "column of interest" if it contains *any* of the colors azure (8), green (3), or red (2).
2.  **Construct Output Grid:** Create a new grid with the same dimensions as the input grid and initialize all values to blue (1).
3.  **Copy and Place Segments:** For each "column of interest", copy the segment of the column starting from the top down to the last non-black pixel that contains either an azure, green or red. Place this segment at the top of the corresponding column in the output grid. If a column has multiple, separate segments of interest, only the top-most is copied.
4. **Return Output Grid**: Return the output grid.
"""

import numpy as np

def get_columns_of_interest(grid):
    # identify columns of interest - with colors 8, 3, 2
    cols_of_interest = []
    for j in range(grid.shape[1]):
        unique_colors = np.unique(grid[:, j])
        if any(color in unique_colors for color in [8, 3, 2]):
            cols_of_interest.append(j)
    return cols_of_interest

def get_segment_to_copy(column):
    # get segment from top to last occurrence of 8, 3, or 2
    indices = np.where(np.isin(column, [8, 3, 2]))[0]
    if len(indices) > 0:
        last_index = indices[-1]
        return column[:last_index+1]
    else:
        return np.array([])

def transform(input_grid):
    # initialize output_grid as all blue (1)
    output_grid = np.ones_like(input_grid)

    # get columns of interest
    cols_of_interest = get_columns_of_interest(input_grid)

    # place segments of columns of interest into output_grid
    for j in cols_of_interest:
      segment = get_segment_to_copy(input_grid[:, j])
      if len(segment) > 0:
          output_grid[:len(segment), j] = segment

    return output_grid