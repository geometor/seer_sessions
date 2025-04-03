import copy

def find_contiguous_blocks(row, color):
    """
    Finds all contiguous blocks of a specified color within a single row.

    Args:
        row (list): A list of integers representing a row of the grid.
        color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple represents a block
              and contains (start_index, end_index, length).
              'end_index' is the index *after* the last pixel of the block.
    """
    blocks = []
    start_index = -1
    n = len(row)
    for i, pixel in enumerate(row):
        # Check if current pixel matches the target color
        if pixel == color:
            # If we are not already in a block, mark the start
            if start_index == -1:
                start_index = i
        # If the pixel does not match the target color
        else:
            # If we were just in a block, it has now ended
            if start_index != -1:
                end_index = i # End index is exclusive
                length = end_index - start_index
                blocks.append((start_index, end_index, length))
                start_index = -1 # Reset start index
                
    # After the loop, check if a block was ongoing until the end of the row
    if start_index != -1:
        end_index = n # End index is exclusive (index after the last element)
        length = end_index - start_index
        blocks.append((start_index, end_index, length))
        
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by finding the longest contiguous horizontal
    block(s) of red (2) pixels in each row and changing their color to 
    magenta (6). Other pixels remain unchanged. If multiple blocks share the 
    maximum length in a row, all of them are changed.

    Args:
        input_grid (list of list of int): The input grid represented as a 
                                           list of rows.

    Returns:
        list of list of int: The transformed grid.
    """
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    
    # Define the colors
    target_color = 2 # red
    new_color = 6    # magenta

    # Iterate through each row of the grid
    for r, row in enumerate(input_grid):
        # Find all contiguous blocks of the target color (red) in the current row
        red_blocks = find_contiguous_blocks(row, target_color)

        # If no red blocks are found in this row, continue to the next row
        if not red_blocks:
            continue

        # Determine the maximum length among all red blocks found in this row
        max_length = 0
        for start, end, length in red_blocks:
            if length > max_length:
                max_length = length
        
        # Iterate through the found red blocks again
        for start, end, length in red_blocks:
            # If a block's length equals the maximum length for this row
            if length == max_length:
                # Change the color of the pixels within that block in the output grid row
                for c in range(start, end):
                    output_grid[r][c] = new_color

    # Return the modified output grid
    return output_grid