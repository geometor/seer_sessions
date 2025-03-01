# 88a62173 • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves extracting the top-left '1' (blue) pixels from each 2x2 block within the input grid that contains at least one '1', and arranging them to form the output grid.
"""

import numpy as np

def get_top_left_ones(grid):
    """
    Finds the top-left '1's in 2x2 blocks of the input grid.
    """
    top_left_ones = []
    height, width = grid.shape
    for r in range(0, height - 1):
        for c in range(0, width - 1):
            block = grid[r:r+2, c:c+2]
            if 1 in block:
                # Find the relative position of the top-left '1' within the block
                ones_indices = np.argwhere(block == 1)
                if len(ones_indices) > 0:
                    top_left_index = tuple(ones_indices[0])
                    # Translate to the absolute coordinates in the original grid
                    top_left_ones_coords = (r + top_left_index[0], c + top_left_index[1])

                    if len(top_left_ones) == 0:
                        top_left_ones.append(top_left_ones_coords)
                    else:
                        exists = False
                        for one in top_left_ones:
                            if one == top_left_ones_coords:
                                exists = True

                        if not exists:
                            top_left_ones.append(top_left_ones_coords)


    return top_left_ones
def transform(input_grid):
    """
    Transforms the input grid into the output grid by extracting the top-left '1's
    from each 2x2 block and arranging them in the output grid.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find the top-left '1's coordinates in the input grid
    top_left_ones = get_top_left_ones(input_grid)

    # Determine the dimensions of the output grid based on unique top-left positions
    if len(top_left_ones) > 0 :
        max_row = max(coord[0] for coord in top_left_ones)
        max_col = max(coord[1] for coord in top_left_ones)
        rows = []
        cols = []
        for coord in top_left_ones:
          rows.append(coord[0])
          cols.append(coord[1])

        output_rows = sorted(list(set(rows)))
        output_cols = sorted(list(set(cols)))

        output_grid = np.zeros((len(output_rows), len(output_cols)), dtype=int)


        # Fill the output grid based on the extracted coordinates
        for i in range(len(output_rows)):
            for j in range(len(output_cols)):
                if (output_rows[i], output_cols[j]) in top_left_ones:
                    output_grid[i, j] = 1
    else:
        output_grid = np.array([])
    return output_grid.tolist()
```
