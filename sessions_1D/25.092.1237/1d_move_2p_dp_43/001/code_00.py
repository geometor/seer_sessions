import collections

"""
Analyze the input sequence (1D list) to identify four distinct, non-overlapping segments:
a. Find the contiguous block of identical pixels whose color is neither white (0) nor blue (1). Call this the `main_block`.
b. Find the contiguous sequence of two white pixels `[0, 0]`. Call this the `white_pair`.
c. Identify the sequence of pixels, if any, that appear *before* the `main_block`. Call this the `prefix`.
d. Identify the sequence of pixels that appear *after* the `white_pair`. Call this the `suffix`.
Construct the output sequence by concatenating these four segments in the following order: `prefix`, `white_pair`, `main_block`, `suffix`.
The resulting concatenated sequence is the final output.
"""

def find_main_block(grid):
    """
    Finds the first contiguous block of identical pixels with color neither 0 nor 1.
    Returns the start index, end index (inclusive), and the color of the block.
    Returns None, None, None if no such block is found.
    """
    start_index = -1
    block_color = -1
    max_len = 0
    current_start = -1
    current_len = 0
    current_color = -1

    for i, color in enumerate(grid):
        if color != 0 and color != 1:
            if color == current_color:
                current_len += 1
            else: # New block potentially starts
                # Check if previous block was a valid main_block candidate
                if current_start != -1:
                    # Found the first valid block, stop searching
                     start_index = current_start
                     block_color = current_color
                     # end index is i-1
                     return start_index, i - 1, block_color

                # Start tracking new potential block
                current_start = i
                current_len = 1
                current_color = color
        else: # color is 0 or 1, breaks any current block
             # Check if previous block was a valid main_block candidate
            if current_start != -1:
                # Found the first valid block, stop searching
                start_index = current_start
                block_color = current_color
                # end index is i-1
                return start_index, i - 1, block_color
            # Reset tracking
            current_start = -1
            current_len = 0
            current_color = -1

    # Check if a block was running until the end of the grid
    if current_start != -1:
         start_index = current_start
         block_color = current_color
         # end index is the last index of the grid
         return start_index, len(grid) - 1, block_color

    # If no block was ever found
    return None, None, None


def find_white_pair(grid):
    """
    Finds the first occurrence of the sequence [0, 0].
    Returns the start index of the pair.
    Returns None if not found.
    """
    for i in range(len(grid) - 1):
        if grid[i] == 0 and grid[i+1] == 0:
            return i
    return None


def transform(input_grid):
    """
    Transforms the input grid based on rearranging identified segments.

    Args:
        input_grid: A list of integers representing the input 1D grid.

    Returns:
        A list of integers representing the transformed output grid.
    """

    # 1. Find the main block (contiguous non-0, non-1 color)
    main_block_start, main_block_end, _ = find_main_block(input_grid)
    if main_block_start is None:
        # Handle error: Main block not found (though examples suggest it exists)
        return input_grid # Or raise an error

    # 2. Find the white pair [0, 0]
    white_pair_start = find_white_pair(input_grid)
    if white_pair_start is None:
         # Handle error: White pair not found (though examples suggest it exists)
        return input_grid # Or raise an error

    # 3. Identify the segments based on the found indices
    #    Note: The description implies white_pair follows main_block, but let's extract
    #    based on identified positions regardless, as long as they don't overlap impossibly.
    #    The example structure is: prefix, main_block, white_pair, suffix

    #    Assuming the structure from examples holds:
    #    prefix is everything before main_block
    #    main_block is from main_block_start to main_block_end
    #    white_pair is from white_pair_start to white_pair_start + 1
    #    suffix is everything after white_pair

    prefix = input_grid[:main_block_start]
    main_block = input_grid[main_block_start : main_block_end + 1]
    white_pair = input_grid[white_pair_start : white_pair_start + 2]
    suffix = input_grid[white_pair_start + 2 :]

    # Check if the assumed structure holds (simple check based on examples)
    # This might need adjustment if the relative order can change
    if main_block_end + 1 != white_pair_start:
        print("Warning: Assumption that white_pair immediately follows main_block might be incorrect for this input.")
        # If the order can truly vary, finding the segments needs more robust logic
        # to handle cases like: prefix, white_pair, ..., main_block, suffix etc.
        # For now, proceed based on the observed example structure and rearrangement rule.


    # 4. Construct the output grid by rearranging
    #    Order: prefix, white_pair, main_block, suffix
    output_grid = prefix + white_pair + main_block + suffix

    return output_grid