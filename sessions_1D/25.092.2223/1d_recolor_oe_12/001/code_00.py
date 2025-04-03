import numpy as np

def transform(input_grid):
    """
    Identifies contiguous horizontal blocks of yellow (4) pixels in the input grid.
    If the length of a yellow block is even, it replaces the pixels in that block with blue (1) in the output grid.
    If the length of a yellow block is odd, it replaces the pixels in that block with magenta (6) in the output grid.
    White (0) pixels remain unchanged.
    Assumes input is effectively 1D (or processes only the first row if multiple rows exist).
    """

    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input grid
    # We will modify the yellow pixels based on the rules
    output_array = np.copy(input_array)

    # Assuming the grid is 1D or we only care about the first row
    # If the input can be genuinely 2D with multiple rows needing this logic,
    # the iteration would need to be adjusted.
    # For ARC tasks, often the pattern applies row-wise or column-wise, 
    # but here the examples are strictly 1D.
    
    rows, cols = output_array.shape
    
    # Iterate through each row (although examples are 1xN)
    for r in range(rows):
        current_block_start = -1
        current_block_length = 0

        # Iterate through columns to find yellow blocks
        for c in range(cols):
            if input_array[r, c] == 4: # Found a yellow pixel
                if current_block_start == -1: # Start of a new block
                    current_block_start = c
                current_block_length += 1
            
            # Check if the block ends (either non-yellow pixel or end of row)
            # Important: check *after* processing the current pixel, 
            # or if we are at the last column
            is_end_of_row = (c == cols - 1)
            ends_block = (input_array[r, c] != 4)

            if current_block_start != -1 and (ends_block or is_end_of_row):
                # Determine the actual end index of the block
                block_end_index = c if ends_block else c + 1 # exclusive end if not end of row
                
                # Apply the transformation rule based on length parity
                replacement_color = 1 if current_block_length % 2 == 0 else 6
                
                # Modify the output array for the identified block
                output_array[r, current_block_start:block_end_index] = replacement_color
                
                # Reset block tracking
                current_block_start = -1
                current_block_length = 0

    # Convert back to list of lists format if necessary (depends on test framework)
    # Assuming the framework expects a numpy array or handles it.
    return output_array.tolist() # Convert back to list of lists for standard ARC format
