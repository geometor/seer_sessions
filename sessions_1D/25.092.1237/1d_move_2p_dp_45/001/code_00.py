import copy

"""
Transformation Rule:
Find a contiguous block of a single color C (where C is not white (0) and not azure (8)). This block must be immediately followed by two white (0) pixels and then immediately by one azure (8) pixel, forming the pattern `[Block C] [0] [0] [8]`. Rearrange this specific segment within the grid to `[0] [0] [Block C] [8]`. All other pixels in the grid remain unchanged.
"""

def find_colored_block(grid):
    """
    Finds the start index, end index, and color of the first contiguous block
    of a color other than white (0) or azure (8).
    Returns (start_index, end_index, color) or (None, None, None) if not found.
    """
    start_index = None
    current_color = None
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 8:
            if start_index is None:
                start_index = i
                current_color = pixel
            elif pixel != current_color: # Found a new block before finishing the old one? This shouldn't happen based on examples.
                 # If we hit a different color block, we assume the previous one ended just before.
                 # However, the logic focuses on the *first* valid block found followed by the pattern.
                 # Reset if the current sequence breaks and doesn't match the expected pattern structure.
                 # Based on the task structure, we expect only one such block relevant to the pattern.
                 # Let's refine this: we are looking for THE block followed by 0,0,8.
                 # We can iterate and check the trailing sequence directly.
                 pass # Continue scanning, the main loop will handle checks
        elif start_index is not None and pixel != current_color : # End of the current block
            end_index = i - 1
            # Check if this block is followed by the required pattern
            if (end_index + 3 < len(grid) and
                grid[end_index + 1] == 0 and
                grid[end_index + 2] == 0 and
                grid[end_index + 3] == 8):
                return start_index, end_index, current_color
            else:
                # This block doesn't fit the pattern, reset and keep searching
                start_index = None
                current_color = None

    # Check if the block extends to the end of the grid
    if start_index is not None:
         end_index = len(grid) - 1
         # Check if the block ends right before the pattern elements would start (impossible pattern)
         if (end_index + 3 < len(grid) and
             grid[end_index + 1] == 0 and
             grid[end_index + 2] == 0 and
             grid[end_index + 3] == 8):
             # This check is slightly redundant due to loop structure, but confirms the end case.
             # The pattern check needs index end_index + 3, so if block goes to end, pattern can't exist after it.
             pass # Redundant Check - The pattern check in the loop handles this implicitly

    # Try a simpler approach: iterate and check pattern *after* finding a potential block end
    start_block = -1
    end_block = -1
    block_color = -1

    for i in range(len(grid)):
        # Potential start of a block
        if grid[i] != 0 and grid[i] != 8 and (i == 0 or (grid[i-1] == 0 or grid[i-1] == 8)):
            start_block = i
            block_color = grid[i]
            # Find the end of this block
            j = i
            while j + 1 < len(grid) and grid[j+1] == block_color:
                j += 1
            end_block = j

            # Check if the pattern [0, 0, 8] follows immediately
            if (end_block + 3 < len(grid) and
                grid[end_block + 1] == 0 and
                grid[end_block + 2] == 0 and
                grid[end_block + 3] == 8):
                # Found the target block and pattern
                return start_block, end_block, block_color

            # If pattern not found, reset and continue scanning
            start_block = -1
            end_block = -1
            block_color = -1

    return None, None, None # Pattern not found


def transform(input_grid):
    """
    Transforms the input grid according to the described rule:
    Finds a sequence [Block C] [0] [0] [8] (C!=0, C!=8) and rearranges
    it to [0] [0] [Block C] [8].
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid) # Use list() for 1D array copy

    # Find the specific colored block followed by the 0, 0, 8 pattern
    start_block, end_block, block_color = find_colored_block(input_grid)

    # If the pattern is found, perform the transformation
    if start_block is not None:
        # Calculate the length of the colored block
        block_length = end_block - start_block + 1

        # Define the indices involved in the segment
        idx_white1 = end_block + 1
        idx_white2 = end_block + 2
        idx_azure = end_block + 3 # This index remains 8

        # Perform the rearrangement in the output grid
        # Place the two white pixels at the beginning of the segment
        output_grid[start_block] = 0
        output_grid[start_block + 1] = 0

        # Place the colored block after the two white pixels
        for i in range(block_length):
            output_grid[start_block + 2 + i] = block_color

        # The azure pixel at idx_azure (which is start_block + 2 + block_length)
        # is already correct in the copied grid, or implicitly set if the copy overwrites it.
        # Let's ensure it's explicitly set for clarity, though copy handles it.
        output_grid[idx_azure] = 8 # Or output_grid[start_block + 2 + block_length] = 8

    # Return the modified grid (or original if pattern wasn't found)
    return output_grid