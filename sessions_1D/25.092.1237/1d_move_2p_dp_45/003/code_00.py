import numpy as np

"""
Transformation Rule:
The input is assumed to be a grid (likely 2D).
1. Flatten the input grid into a 1D sequence.
2. Scan the 1D sequence to find the first occurrence of a pattern: a contiguous block of a single color C (where C is not white (0) and not azure (8)), immediately followed by two white (0) pixels, and then immediately by one azure (8) pixel. The pattern is `[Block C] [0] [0] [8]`.
3. If this pattern is found:
    a. Let the block start at index `start_block` and end at `end_block`.
    b. Rearrange the segment from `start_block` to `end_block + 3` in the 1D sequence.
    c. The new arrangement for this segment becomes `[0] [0] [Block C] [8]`. The block C retains its original length.
4. If the pattern is not found, the grid remains unchanged.
5. Reshape the modified 1D sequence back into the original dimensions of the input grid.
"""

def find_pattern_indices(grid_1d):
    """
    Finds the start index, end index, and color of the first block
    that matches the pattern: [Block C][0][0][8] where C!=0 and C!=8.

    Args:
        grid_1d: A 1D list or numpy array representing the flattened grid.

    Returns:
        A tuple (start_block, end_block, block_color) if the pattern is found.
        Otherwise, returns (None, None, None).
    """
    n = len(grid_1d)
    for i in range(n):
        # Check for the potential start of a block (C != 0 and C != 8)
        if grid_1d[i] != 0 and grid_1d[i] != 8:
            start_block = i
            block_color = grid_1d[i]
            
            # Find the end of the contiguous block of the same color
            j = i
            while j + 1 < n and grid_1d[j + 1] == block_color:
                j += 1
            end_block = j

            # Check if the required pattern [0, 0, 8] follows the block
            # Ensure there are enough elements remaining in the grid for the pattern
            if end_block + 3 < n:
                if (grid_1d[end_block + 1] == 0 and
                    grid_1d[end_block + 2] == 0 and
                    grid_1d[end_block + 3] == 8):
                    # Pattern found, return its details
                    return start_block, end_block, block_color
            
            # If pattern didn't match, continue scanning from the element after this block
            # The outer loop's increment will handle moving forward correctly.
            # No need to explicitly set i = end_block + 1, loop does this.

    # If the loop completes without finding the pattern
    return None, None, None

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Store original shape
    original_shape = input_grid.shape

    # Flatten the input grid to a 1D array
    grid_1d = input_grid.flatten().tolist() # Work with a list for easier modification

    # Create a copy to modify for the output
    output_1d = list(grid_1d)

    # Find the pattern [Block C][0][0][8]
    start_block, end_block, block_color = find_pattern_indices(grid_1d)

    # If the pattern was found, perform the rearrangement
    if start_block is not None:
        # Calculate the length of the colored block
        block_length = end_block - start_block + 1

        # Define the index of the azure marker
        idx_azure = end_block + 3

        # Perform the rearrangement in the output list
        # Place the two white pixels at the beginning of the segment
        output_1d[start_block] = 0
        output_1d[start_block + 1] = 0

        # Place the colored block after the two white pixels
        for i in range(block_length):
            output_1d[start_block + 2 + i] = block_color

        # Place the azure pixel at the end of the rearranged segment
        # The index for the azure pixel in the *new* sequence is start_block + 2 + block_length
        output_1d[start_block + 2 + block_length] = 8
        # Note: The original element at idx_azure was already 8, but this explicitly sets
        # the element at the correct *new* position for the azure marker.

    # Convert the modified list back to a numpy array
    output_array = np.array(output_1d)

    # Reshape the 1D output array back to the original grid shape
    output_grid = output_array.reshape(original_shape)

    return output_grid