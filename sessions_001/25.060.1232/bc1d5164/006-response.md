# bc1d5164 • 006 • refine_coder

---
```python
"""
Extracts the smallest rectangle from the input grid that contains all non-black
pixels, that are not part of any larger object of the same color.
"""

import numpy as np

def get_bounding_box(grid, significant_pixels):
    """
    Calculates the bounding box coordinates for the significant pixels.
    """
    rows, cols = [], []
    for r, c in significant_pixels:
        rows.append(r)
        cols.append(c)

    if not rows or not cols:  # Handle the case where there are no significant pixels
        return 0, -1, 0, -1 # Return an empty bounding box

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def find_significant_pixels(grid):
    """
    Identifies significant pixels, which are non-black pixels not part of a larger uniform area.
    For simplicity, we check if neighboring horizontal and vertical cell are the same
    """

    significant_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                color = grid[r,c]
                # Check if the pixel is part of larger object.
                is_part_of_larger_object = False

                #check up
                if r > 0 and grid[r-1, c] == color:
                    is_part_of_larger_object = True

                #check down
                if r < rows - 1 and grid[r+1, c] == color:
                    is_part_of_larger_object = True

                #check left
                if c > 0 and grid[r, c-1] == color:
                    is_part_of_larger_object = True

                #check right
                if c < cols - 1 and grid[r, c+1] == color:
                    is_part_of_larger_object = True

                if not is_part_of_larger_object:
                    significant_pixels.append((r, c))
    return significant_pixels

def transform(input_grid):
    """
    Transforms the input grid by extracting the bounding box containing all significant pixels.
    """
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Find significant pixels
    significant_pixels = find_significant_pixels(input_array)

    # Find the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(input_array, significant_pixels)

    # Extract the subgrid
    output_grid = input_array[min_row:max_row+1, min_col:max_col+1]

    return output_grid.tolist()
```
