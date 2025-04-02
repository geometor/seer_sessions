import numpy as np

"""
Transforms the input grid by conceptually dividing it into a 3x3 grid of nine 
rectangular regions. The regions might have slightly different dimensions due 
to integer division of the grid's height and width by 3. The content (pixels) 
of each input region is copied to a different region in the output grid 
according to a fixed permutation map. The output grid has the same dimensions 
as the input grid.

The permutation map (input region index (row, col) -> output region index (row, col)), 
using 0-based indexing, is:
(0,0) -> (0,0)
(0,1) -> (0,2)
(0,2) -> (1,0)
(1,0) -> (1,1)
(1,1) -> (1,2)
(1,2) -> (2,1)
(2,0) -> (2,2)
(2,1) -> (2,0)
(2,2) -> (0,1)
"""

def transform(input_grid):
    """
    Permutes the content of a 3x3 division of the input grid based on a fixed map.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed grid.
    """
    # Convert input list of lists to numpy array for efficient slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Get dimensions of the input grid
    H, W = input_np.shape

    # Initialize the output grid with the same dimensions, filled with zeros.
    # The permutation will overwrite these values completely.
    output_np = np.zeros_like(input_np)

    # Calculate the row and column division points for the 3x3 grid layout.
    # These points define the start of the second and third row/column of regions.
    r1 = H // 3
    r2 = 2 * H // 3
    c1 = W // 3
    c2 = 2 * W // 3

    # Define the list of row start and end points for the 3 region rows.
    # The boundaries define slices [start:end].
    row_boundaries = [0, r1, r2, H]
    
    # Define the list of column start and end points for the 3 region columns.
    col_boundaries = [0, c1, c2, W]

    # Define the fixed permutation map: 
    # Key: (input_row_index, input_col_index)
    # Value: (output_row_index, output_col_index)
    # Using 0-based indices for rows and columns (0, 1, 2).
    permutation_map = {
        (0, 0): (0, 0),
        (0, 1): (0, 2),
        (0, 2): (1, 0),
        (1, 0): (1, 1),
        (1, 1): (1, 2),
        (1, 2): (2, 1),
        (2, 0): (2, 2),
        (2, 1): (2, 0),
        (2, 2): (0, 1)
    }

    # Iterate through the 3x3 grid regions of the input
    for r_in in range(3):
        for c_in in range(3):
            # Determine the pixel boundaries for the current input region
            start_row_in = row_boundaries[r_in]
            end_row_in = row_boundaries[r_in + 1]
            start_col_in = col_boundaries[c_in]
            end_col_in = col_boundaries[c_in + 1]

            # Extract the subgrid data (pixels) from the input region
            input_subgrid = input_np[start_row_in:end_row_in, start_col_in:end_col_in]

            # Get the corresponding output region indices using the permutation map
            r_out, c_out = permutation_map[(r_in, c_in)]

            # Determine the pixel coordinates for the top-left corner of the target output region
            start_row_out = row_boundaries[r_out]
            start_col_out = col_boundaries[c_out]
            
            # Determine the expected dimensions of the output region slice
            # This ensures that even if regions have slightly different sizes,
            # we paste correctly into the target region's space.
            end_row_out = row_boundaries[r_out + 1]
            end_col_out = col_boundaries[c_out + 1]
            
            # Check if the shapes match (should always match if boundaries are calculated correctly)
            # target_height = end_row_out - start_row_out
            # target_width = end_col_out - start_col_out
            # if input_subgrid.shape[0] != target_height or input_subgrid.shape[1] != target_width:
                 # This case should ideally not happen with the current logic
                 # Handle error or adjust slicing if needed, though unlikely here.
                 # print(f"Warning: Shape mismatch for region ({r_in},{c_in}) -> ({r_out},{c_out})")
                 # print(f"Input shape: {input_subgrid.shape}, Target shape: ({target_height}, {target_width})")
                 # Adjust paste dimensions if necessary, e.g., clip input_subgrid if larger
                 # clipped_subgrid = input_subgrid[:target_height, :target_width]
                 # output_np[start_row_out:end_row_out, start_col_out:end_col_out] = clipped_subgrid

            # Paste the extracted input subgrid into the output grid at the calculated target location.
            # The slice size in the output grid is defined by the target region's boundaries.
            output_np[start_row_out:end_row_out, start_col_out:end_col_out] = input_subgrid

    # Convert the final numpy array back to a standard list of lists format
    return output_np.tolist()