import copy

# Helper function definitions (as derived in thought process)

def find_fill_block(grid):
    """
    Finds the first contiguous block of non-white (0), non-azure (8) pixels
    in the 1D grid.
    Returns a tuple (start_index, end_index, fill_color) if found,
    otherwise returns None.
    """
    for i in range(len(grid)):
        pixel = grid[i]
        # Check if the pixel is a potential start of the fill block
        if pixel != 0 and pixel != 8:
            fill_color = pixel
            start_index = i
            end_index = i
            # Extend the end index forward as long as the color matches
            j = i + 1
            while j < len(grid) and grid[j] == fill_color:
                end_index = j
                j += 1
            # Return the details of the found block immediately
            return start_index, end_index, fill_color
    # Return None if no such block is found after checking the entire grid
    return None

def find_azure_pixel(grid, start_search_index):
    """
    Finds the index of the first azure (8) pixel at or after the
    specified start_search_index in the 1D grid.
    Returns the index if found, otherwise returns -1.
    """
    for i in range(start_search_index, len(grid)):
        if grid[i] == 8:
            return i
    # Return -1 if no azure pixel is found from the start index onwards
    return -1


# Main transform function
def transform(input_grid):
    """
    Transforms the input grid (1D array) according to the rule:
    1. Identify a contiguous block of a single color, where the color is
       not white (0) and not azure (8).
    2. Find the first azure (8) pixel occurring after this block.
    3. Change the color of all pixels located strictly between the end of
       the identified block and the azure pixel to match the block's color.
    4. Leave all other pixels in the grid unchanged.

    Args:
        input_grid (list): A list of integers representing the 1D input grid.

    Returns:
        list: A list of integers representing the transformed 1D output grid.
    """
    # Create a copy of the input grid to modify.
    # list() constructor performs a shallow copy, sufficient for a 1D list of ints.
    output_grid = list(input_grid)

    # Step 1: Identify the contiguous block of non-white, non-azure color.
    # This uses the find_fill_block helper function.
    block_info = find_fill_block(output_grid)

    # If no such block is found, the transformation cannot proceed as described.
    # Based on the task examples, such a block is always present.
    # We return the unmodified grid copy in this unlikely case.
    if block_info is None:
        print("Warning: No fill block found.")
        return output_grid

    # Unpack the block information.
    _start_fill_index, end_fill_index, fill_color = block_info # _start is unused later

    # Step 2: Find the index of the first azure pixel after the block ends.
    # The search starts from the index immediately following the block's end index.
    azure_index = find_azure_pixel(output_grid, end_fill_index + 1)

    # If no azure pixel is found after the block, the transformation cannot proceed.
    # Based on task examples, an azure pixel is always present after the block.
    # Return the unmodified grid copy in this unlikely case.
    if azure_index == -1:
        print("Warning: No azure pixel found after fill block.")
        return output_grid

    # Step 3: Fill the gap between the block and the azure pixel.
    # Iterate through the indices strictly between the end of the block
    # and the azure pixel's index.
    for i in range(end_fill_index + 1, azure_index):
        # Change the color of the pixel at the current index to the fill_color.
        # No check for the original color (e.g., white) is needed as per description;
        # all pixels in this range are overwritten.
        output_grid[i] = fill_color

    # Step 4: All other pixels (before the block, the block itself, the azure pixel,
    # and pixels after the azure pixel) remain unchanged because we started with a copy
    # and only modified the pixels within the calculated range.

    # Return the modified grid.
    return output_grid