```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by identifying contiguous horizontal blocks of azure (8) pixels.
    If a block has an odd length, it's replaced with red (2).
    If a block has an even length, it's replaced with maroon (9).
    White (0) pixels remain unchanged.
    Assumes the input grid is a single row (1xN).
    """

    # Input is expected as list of lists, extract the single row
    # Handle potential numpy array input gracefully
    if isinstance(input_grid, np.ndarray):
        input_row = input_grid.tolist()[0]
    else:
        input_row = input_grid[0]

    # Initialize output_row as a copy of the input_row
    output_row = list(input_row)
    grid_width = len(input_row)

    # Iterate through the row to find azure blocks
    current_block_start = -1
    for i in range(grid_width):
        # Check if the current pixel is azure (8)
        is_azure = (input_row[i] == 8)

        # If it's azure and we are not already tracking a block, mark the start
        if is_azure and current_block_start == -1:
            current_block_start = i

        # Check if the block ends here (either pixel is not azure or it's the end of the row)
        # We must have been inside a block (current_block_start != -1)
        if current_block_start != -1 and (not is_azure or i == grid_width - 1):
            # Determine the correct end index for slicing/length calculation
            # If the loop ended because we hit a non-azure pixel, the block ended *before* i
            # If the loop ended because we hit the end of the grid AND the last pixel was azure, the block ends *at* i (inclusive)
            block_end_exclusive = i if not is_azure else i + 1

            # Calculate the length of the identified azure block
            block_length = block_end_exclusive - current_block_start

            # Determine the replacement color based on length parity
            if block_length % 2 != 0: # Odd length
                replacement_color = 2 # red
            else: # Even length
                replacement_color = 9 # maroon

            # Modify the output_row, replacing the azure block with the determined color
            for j in range(current_block_start, block_end_exclusive):
                output_row[j] = replacement_color

            # Reset the block start marker
            current_block_start = -1

    # Wrap the modified row back into the list of lists format
    output_grid = [output_row]

    # Return the transformed grid
    return output_grid
```