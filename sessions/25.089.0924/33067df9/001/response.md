```python
import numpy as np

"""
Transforms an input grid containing sparse colored pixels into a 26x26 output grid.
The output grid has a 2-pixel white border. The inner 22x22 area displays 
solid-colored blocks corresponding to the non-white pixels in the input. 
The relative positions of the input pixels determine the layout of the blocks 
in the output. The size of each block is uniform and calculated based on the 
number of input rows and columns that contain non-white pixels, ensuring they fit 
within the 22x22 area with 2-pixel gaps between them.
"""

def find_active_indices(grid):
    """Finds unique row and column indices containing non-white pixels."""
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return [], []
    active_rows = sorted(list(np.unique(non_white_coords[:, 0])))
    active_cols = sorted(list(np.unique(non_white_coords[:, 1])))
    return active_rows, active_cols

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid)
    
    # Constants for the output grid layout
    output_size = 26
    active_area_dim = 22
    border_offset = 2
    gap_size = 2

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # 1. Find active rows and columns in the input grid
    active_rows, active_cols = find_active_indices(input_np)
    N_rows = len(active_rows)
    N_cols = len(active_cols)

    # If there are no non-white pixels, return the empty grid
    if N_rows == 0 or N_cols == 0:
        return output_grid.tolist() # Return as list of lists

    # 2. Calculate the dimensions of the output blocks
    # Ensure division results in integers
    block_height = (active_area_dim - (N_rows - 1) * gap_size) // N_rows
    block_width = (active_area_dim - (N_cols - 1) * gap_size) // N_cols

    # 3. Create mappings from input row/col index to output block index
    row_map = {r: i for i, r in enumerate(active_rows)}
    col_map = {c: j for i, c in enumerate(active_cols)}

    # 4. Iterate through input grid and draw blocks in the output grid
    input_rows, input_cols = input_np.shape
    for r in range(input_rows):
        for c in range(input_cols):
            color = input_np[r, c]
            # If the pixel is not white
            if color != 0:
                # Find the corresponding block's position index (i, j)
                i = row_map[r]
                j = col_map[c]

                # Calculate the top-left corner coordinates for the output block
                out_r_start = border_offset + i * (block_height + gap_size)
                out_c_start = border_offset + j * (block_width + gap_size)
                
                # Calculate the bottom-right corner coordinates (exclusive)
                out_r_end = out_r_start + block_height
                out_c_end = out_c_start + block_width

                # Fill the block in the output grid
                output_grid[out_r_start:out_r_end, out_c_start:out_c_end] = color

    # Return the final grid as a list of lists
    return output_grid.tolist()
```