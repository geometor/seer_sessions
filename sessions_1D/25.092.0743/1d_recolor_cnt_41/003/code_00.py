import copy

"""
Replace contiguous horizontal blocks of yellow (4) pixels in a single-row grid with a new color determined by the block's length. Blocks of length 1 become maroon (9), length 2 become magenta (6), and length 3 become green (3). White (0) pixels remain unchanged.
"""

def find_and_replace_yellow_blocks(row):
    """
    Identifies contiguous blocks of yellow (4) pixels in a row and replaces
    them based on their length according to the mapping: 1->9, 2->6, 3->3.

    Args:
        row (list): A list of integers representing a single row of the grid.

    Returns:
        list: The modified row with yellow blocks replaced.
    """
    output_row = list(row) # Create a copy to modify
    width = len(row)
    col = 0
    while col < width:
        # Check if the current pixel is yellow (4)
        if row[col] == 4:
            # Found the start of a potential yellow block
            start_col = col
            block_length = 0
            # Count consecutive yellow pixels
            while col < width and row[col] == 4:
                block_length += 1
                col += 1 # Advance main pointer as we count

            # Determine the replacement color based on block length
            replacement_color = -1 # Sentinel value for no replacement defined
            if block_length == 1:
                replacement_color = 9 # Maroon
            elif block_length == 2:
                replacement_color = 6 # Magenta
            elif block_length == 3:
                replacement_color = 3 # Green
            
            # Apply the replacement color to the output row for the identified block
            # Slicing works as [start_col:col] because 'col' is already one position
            # *after* the end of the block due to the inner while loop.
            if replacement_color != -1:
                for i in range(start_col, col):
                    output_row[i] = replacement_color
            
            # The loop variable 'col' is already advanced past the block,
            # so the outer loop will continue correctly from the next pixel.
            continue # Skip the increment at the end of the main loop body

        # If the current pixel is not yellow, move to the next column
        col += 1
        
    return output_row

def transform(input_grid):
    """
    Transforms the input grid by replacing yellow blocks based on length.

    Args:
        input_grid (list[list[int]]): A list containing a single list representing the 1xN input grid.

    Returns:
        list[list[int]]: A list containing a single list representing the transformed 1xN output grid.
    """
    # Ensure input is in the expected format (list of lists) and handle potential errors
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
        # Handle error case or return input unchanged, depending on requirements
        # For now, assume valid input as per ARC examples.
        # You might want to add more robust error handling here.
        print("Warning: Unexpected input grid format.")
        return copy.deepcopy(input_grid) # Return a copy to avoid modifying original

    # Extract the single row (input guaranteed to be 1xN based on examples)
    input_row = input_grid[0]
    
    # Process the row to find and replace yellow blocks
    output_row = find_and_replace_yellow_blocks(input_row)

    # Wrap the modified row back into the list-of-lists structure
    output_grid = [output_row]
    
    return output_grid
