import copy

"""
Processes a 2D grid of integers (0, 3, 8). 
For each row independently, it identifies contiguous blocks of the number 3.
Each block of 3s is moved as far left as possible within its row.
The movement stops if the block hits the beginning of the row (column 0) or if the cell immediately to the left of the block's intended new position contains a non-zero value (specifically 8, acting as a barrier).
When a block moves, its original position is filled with 0s, and the destination cells (which must have been 0s) are filled with 3s.
The processing of blocks within a row occurs from right to left.
"""

def find_block_start(row: list[int], end_index: int) -> int:
    """Finds the starting index of a contiguous block of 3s ending at end_index."""
    start_index = end_index
    while start_index > 0 and row[start_index - 1] == 3:
        start_index -= 1
    return start_index

def find_destination(row: list[int], block_start_index: int) -> int:
    """Finds the leftmost possible starting column for the block."""
    dest_index = block_start_index
    check_index = block_start_index - 1
    while check_index >= 0:
        # If the cell to the left is not 0, the block stops just after it.
        if row[check_index] != 0:
            dest_index = check_index + 1
            break
        # If the cell to the left is 0, the block can potentially move there.
        dest_index = check_index
        check_index -= 1
    # If the loop finishes without finding a barrier, the destination is column 0.
    return dest_index

def process_row(row: list[int]) -> list[int]:
    """Applies the block moving transformation to a single row."""
    output_row = list(row) # Work on a copy
    width = len(output_row)
    j = width - 1 # Start scanning from the right

    while j >= 0:
        # Check if the current cell is the end of a block of 3s
        if output_row[j] == 3:
            # Find the start of this block
            start_col = find_block_start(output_row, j)
            block_length = j - start_col + 1

            # Determine where this block should move to
            dest_col = find_destination(output_row, start_col)

            # If the block needs to move
            if dest_col != start_col:
                # Clear the original position
                for i in range(start_col, start_col + block_length):
                    output_row[i] = 0
                # Place the block at the new destination
                for i in range(dest_col, dest_col + block_length):
                    output_row[i] = 3

            # Move the scan index to the left of the processed block
            j = start_col - 1
        else:
            # Move to the next cell to the left
            j -= 1
            
    return output_row


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by moving blocks of 3s leftwards in each row
    until they hit a barrier (8) or the start of the row.
    """
    # Initialize output_grid as a deep copy to avoid modifying the input directly
    # Although process_row works on copies, this ensures rows not needing processing are still new objects.
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Process the row to move the blocks of 3s
        processed_row = process_row(row)
        # Add the processed row to the output grid
        output_grid.append(processed_row)

    # Return the completely transformed grid
    return output_grid
