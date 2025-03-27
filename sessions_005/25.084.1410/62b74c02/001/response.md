```python
import numpy as np

def find_first_all_white_column(grid_np):
    """Finds the index of the first column containing only white pixels (0)."""
    height, width = grid_np.shape
    for c in range(width):
        if np.all(grid_np[:, c] == 0):
            return c
    # If no all-white column is found, return the grid width
    return width

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identifies an initial non-white block starting at the top-left (column 0).
    2. Preserves this initial block in the output grid.
    3. Fills the remaining columns (originally white) to the right.
    4. The rightmost columns of the output are filled by mirroring the columns
       of the initial block (last block column goes to last output column, etc.).
    5. Any columns between the initial block and the mirrored section are filled
       by repeating the first column of the initial block.
    """
    
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, grid_width = input_np.shape

    # Find the width (W) of the initial non-white block
    # W is the index of the first column that is entirely white (0)
    initial_block_width = find_first_all_white_column(input_np)

    # Handle the edge case where the entire grid is the initial block
    if initial_block_width == grid_width:
        # If there's no white region, the output is identical to the input
        return input_grid 
        
    # Initialize the output grid as a copy of the input grid.
    # This preserves the initial block automatically.
    output_np = np.copy(input_np)

    # Rule Part 1: Map columns in reverse order to the right end
    # Iterate from i = 0 up to initial_block_width - 1
    # Copy column (initial_block_width - 1 - i) from input 
    # to column (grid_width - 1 - i) in output
    for i in range(initial_block_width):
        source_col_index = initial_block_width - 1 - i
        target_col_index = grid_width - 1 - i
        
        # Ensure target index is valid (should always be if logic is correct)
        if target_col_index >= initial_block_width:
             output_np[:, target_col_index] = input_np[:, source_col_index]
        # If target_col_index < initial_block_width, it means GridW < 2*W, 
        # and this mirrored column would overwrite part of the original block. 
        # The problem description implies the original block is preserved, 
        # and the examples don't show this overlap causing overwrites *within* the original block area.
        # However, the logic inherently handles this as the target index calculation is correct.
        # Let's stick to the direct calculation.
        # Re-checking examples: they don't seem to have GridW < 2*W.
        # The logic should be correct: fill from right to left.
        output_np[:, target_col_index] = input_np[:, source_col_index]


    # Rule Part 2: Fill the middle columns with the first column of the initial block
    # These are columns from index initial_block_width up to (grid_width - initial_block_width - 1)
    # The range starts at W and ends just before the mirrored part begins (at GridW - W).
    # The last index to fill is grid_width - initial_block_width - 1.
    first_column_of_block = input_np[:, 0]
    for j in range(initial_block_width, grid_width - initial_block_width):
        output_np[:, j] = first_column_of_block

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid

```