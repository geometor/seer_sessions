import numpy as np
from typing import List

"""
Transforms an input grid composed of solid-colored rectangular blocks into a smaller 
output grid where each cell represents one block from the input. 
The output grid's dimensions correspond to the number of block rows and columns 
in the input. The color of each output cell matches the color of the corresponding 
input block, preserving the relative spatial arrangement.

Workflow:
1. Convert the input list of lists into a NumPy array.
2. Identify the top-left corner coordinates (row, column) and the color of each 
   distinct rectangular block in the input grid. A pixel is considered a top-left 
   corner if its color differs from the pixel above it (or if it's in the first row) 
   AND its color differs from the pixel to its left (or if it's in the first column).
3. Determine the dimensions of the output grid:
   - Collect and sort the unique row coordinates of the identified top-left corners. 
     The number of unique rows is the output height.
   - Collect and sort the unique column coordinates of the identified top-left corners. 
     The number of unique columns is the output width.
4. Create an empty output grid (NumPy array) with the determined dimensions.
5. Populate the output grid: For each identified block (represented by its top-left 
   corner row, column, and color):
   - Find the index of the block's row in the sorted unique row list. This is the 
     output row index.
   - Find the index of the block's column in the sorted unique column list. This 
     is the output column index.
   - Assign the block's color to the output grid at the calculated (output row, 
     output column) position.
6. Convert the completed NumPy output grid back into a list of lists and return it.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Summarizes a grid of colored rectangular blocks into a smaller grid 
    representing the block layout and colors.
    """
    # Convert input to NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Store top-left corners: (row, col, color)
    top_left_corners = []
    # Store unique row and column indices of corners
    corner_rows = set()
    corner_cols = set()

    # --- 1. Identify Block Top-Left Corners ---
    for r in range(height):
        for c in range(width):
            # Check if the pixel above has a different color (or if it's the first row)
            is_top_edge = (r == 0) or (input_np[r, c] != input_np[r - 1, c])
            # Check if the pixel to the left has a different color (or if it's the first column)
            is_left_edge = (c == 0) or (input_np[r, c] != input_np[r, c - 1])

            # If it's both a top edge and a left edge relative to color changes, it's a top-left corner
            if is_top_edge and is_left_edge:
                color = input_np[r, c]
                top_left_corners.append({'r': r, 'c': c, 'color': color})
                corner_rows.add(r)
                corner_cols.add(c)

    # --- 2. Determine Output Dimensions ---
    # Sort the unique row and column coordinates to map them to output indices
    sorted_corner_rows = sorted(list(corner_rows))
    sorted_corner_cols = sorted(list(corner_cols))
    
    output_height = len(sorted_corner_rows)
    output_width = len(sorted_corner_cols)

    # Create mapping from corner coordinate to output index
    row_map = {r: i for i, r in enumerate(sorted_corner_rows)}
    col_map = {c: i for i, c in enumerate(sorted_corner_cols)}

    # --- 3. Create Output Grid ---
    # Initialize with a placeholder value like -1 or use default 0 if 0 is not a possible block color (it isn't in ARC generally)
    output_np = np.zeros((output_height, output_width), dtype=int) 

    # --- 4. Populate Output Grid ---
    for corner in top_left_corners:
        output_row = row_map[corner['r']]
        output_col = col_map[corner['c']]
        output_np[output_row, output_col] = corner['color']

    # --- 5. Return Output ---
    # Convert back to list of lists format
    output_grid = output_np.tolist()
    
    return output_grid