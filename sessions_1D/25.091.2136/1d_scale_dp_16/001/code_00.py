import copy

"""
Identify the magenta '6' pixel (marker).
Identify the last contiguous block of a single non-white color that occurs immediately before the marker, possibly separated by white '0' pixels.
Determine the color of this block.
Fill all the white '0' pixels located between the end of this block and the marker pixel with the block's color.
Leave all other pixels unchanged.
"""

def find_marker_index(grid_1d):
    """Finds the index of the first magenta (6) pixel."""
    try:
        return grid_1d.index(6)
    except ValueError:
        # Handle cases where the marker is not found, although examples suggest it always exists.
        return -1 

def find_fill_block_and_color(grid_1d, marker_idx):
    """
    Finds the start index, end index, and color of the relevant non-white block.
    Searches backwards from the marker.
    """
    block_end_idx = -1
    fill_color = -1

    # Search backwards from marker_idx - 1 to find the end of the block (first non-white pixel)
    for i in range(marker_idx - 1, -1, -1):
        if grid_1d[i] != 0:
            block_end_idx = i
            fill_color = grid_1d[i]
            break
    
    if block_end_idx == -1:
        # No non-white block found before the marker
        return -1, -1, -1

    # Search backwards from block_end_idx - 1 to find the start of the block (first white pixel or start of list)
    block_start_idx = block_end_idx # Assume block is single pixel initially
    for i in range(block_end_idx - 1, -1, -1):
        if grid_1d[i] == fill_color:
             block_start_idx = i
        elif grid_1d[i] == 0: # Found the white pixel preceding the block
             break
        else: # Found a pixel of a different non-white color, block ends here
             break
    else: 
         # if loop completed without break, means block potentially starts at index 0
         if grid_1d[0] == fill_color:
            block_start_idx = 0

    # Check if the identified start actually has the fill color
    if grid_1d[block_start_idx] != fill_color:
        # This case should ideally not happen if block_end_idx was correctly identified,
        # but handles edge case like [0, 2, 0, 6] where block is just '2' at index 1.
        # Re-evaluate based on block_end_idx
        if grid_1d[block_end_idx] == fill_color:
             block_start_idx = block_end_idx # block is a single pixel


    return block_start_idx, block_end_idx, fill_color


def transform(input_grid):
    """
    Transforms the input 1D grid based on the rule:
    Fill the white gap between the last non-white block and the marker '6'
    with the color of that block.
    """
    # Ensure input is treated as a 1D list (flatten if necessary, though examples are 1D)
    if isinstance(input_grid, list) and all(isinstance(row, list) for row in input_grid):
         # Assuming it's a grid with one row based on examples
         if len(input_grid) == 1:
              grid_1d = input_grid[0]
         else:
              # Handle unexpected multi-row grids if necessary, or raise error
              # For now, assume it's always effectively 1D as per examples
              # Flattening might be an option: grid_1d = [cell for row in input_grid for cell in row]
              # Based on example format, let's assume input_grid *is* the 1D list
              grid_1d = input_grid 
    elif isinstance(input_grid, list):
         grid_1d = input_grid # Already a 1D list
    else:
        raise TypeError("Input must be a list (representing a 1D grid)")

    # Create a copy to modify
    output_grid_1d = list(grid_1d)

    # 1. Find the marker index
    marker_idx = find_marker_index(output_grid_1d)
    if marker_idx == -1:
        # If no marker, return the original grid (or handle as error)
        return output_grid_1d 

    # 2. Find the fill block details (start, end, color) searching backwards from marker
    block_start_idx, block_end_idx, fill_color = find_fill_block_and_color(output_grid_1d, marker_idx)

    # Check if a valid block was found
    if block_end_idx == -1 or fill_color == -1:
        # No suitable block found before the marker, return original
        return output_grid_1d

    # 3. Fill the gap between the block end and the marker
    # The gap starts at the index immediately after the block ends
    gap_start_idx = block_end_idx + 1
    # The gap ends at the index immediately before the marker
    gap_end_idx = marker_idx

    # Iterate through the indices within the gap
    for i in range(gap_start_idx, gap_end_idx):
        # If the pixel in the gap is white (0)
        if output_grid_1d[i] == 0:
            # Change its color to the fill color
            output_grid_1d[i] = fill_color

    # Return the modified 1D list
    # If the original input was nested like [[...]], return it in the same format
    if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
         return [output_grid_1d] 
    else:
         return output_grid_1d