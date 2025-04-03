"""
Transforms a 1xN input grid by rearranging elements within the single row. 
It identifies a single marker pixel (color 9) and a contiguous block of 
another color (non-0, non-9). The marker pixel maintains its original column 
index. The colored block is moved to the position immediately following the 
marker, preserving the length of any gap of background pixels (color 0) 
that originally existed between the block and the marker. In the output row, 
the marker is followed by the gap (if any), which is then followed by the 
colored block. The background color is white (0).
"""

import numpy as np

def find_marker_in_row(row_array):
    """
    Finds the column index of the marker pixel (9) in a 1D numpy array (row).
    Returns the index, or -1 if not found.
    """
    # Find indices where the value is 9
    marker_indices = np.where(row_array == 9)[0]
    # Assume only one marker based on examples
    if len(marker_indices) > 0:
        return marker_indices[0] 
    return -1 # Marker not found

def find_colored_block_in_row(row_array):
    """
    Finds the start index, end index, and color of the contiguous 
    non-background (0), non-marker (9) block in a 1D numpy array (row).
    Returns (start_index, end_index, color), or (-1, -1, -1) if not found.
    """
    block_start = -1
    block_end = -1
    block_color = -1
    
    # Iterate through the row to find the block
    for i, pixel in enumerate(row_array):
        # Check if the pixel is part of the colored block (not 0 and not 9)
        if pixel != 0 and pixel != 9:
            if block_start == -1:
                # Found the start of a potential block
                block_start = i
                block_color = pixel
            # Check if this is the end of the block
            # End conditions: end of row OR next pixel is not the block color
            if (i + 1 == len(row_array) or row_array[i+1] != block_color):
                 block_end = i
                 # Found the complete block, return its properties
                 return block_start, block_end, block_color
        elif block_start != -1:
             # This handles cases where a block was started but interrupted
             # by 0 or 9. The previous check should catch the end correctly.
             # If we reach here, it implies the block ended at the previous index.
             # However, the logic inside the main 'if' handles contiguous blocks.
             pass 

    # If no block was found after iterating through the whole row
    return block_start, block_end, block_color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid (assumed 1xN).
    
    Args:
        input_grid (list of lists): A 1xN grid represented as a list containing one list.

    Returns:
        list of lists: The transformed 1xN grid.
    """
    
    # Validate input format and extract the single row
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list) or len(input_grid) != 1:
        # Return input unchanged or raise error if format is incorrect
        # For ARC, it's usually better to return input if rules don't apply clearly
        # print("Warning: Input grid format is not 1xN. Returning input.")
        return input_grid
        
    input_row = input_grid[0]
    # Convert row to numpy array for easier manipulation
    input_row_array = np.array(input_row, dtype=int)
    row_size = len(input_row_array)
    
    # Initialize output_row with background color (0)
    output_row_array = np.zeros_like(input_row_array)

    # 1. Locate the single marker pixel (maroon, 9) and note its index
    marker_index = find_marker_in_row(input_row_array)
    # If no marker, return original grid (or an empty grid of same size?)
    # Based on examples, marker always exists.
    if marker_index == -1:
        # print("Warning: Marker (9) not found. Returning input.")
        return input_grid 

    # 2. Locate the contiguous colored block (not 0 or 9)
    block_start_index, block_end_index, block_color = find_colored_block_in_row(input_row_array)
    # If no block, place marker and return
    if block_start_index == -1:
        # print("Warning: Colored block not found. Placing marker only.")
        output_row_array[marker_index] = 9
        return [output_row_array.tolist()]

    # Calculate block length
    block_length = block_end_index - block_start_index + 1

    # 3. Determine the gap length between the block end and the marker start
    # Assumes block is always before marker as per examples
    gap_start_index_in_input = block_end_index + 1
    gap_end_index_in_input = marker_index - 1 
    gap_length = 0
    if gap_start_index_in_input <= gap_end_index_in_input:
         # Calculate number of elements in the gap
         gap_length = gap_end_index_in_input - gap_start_index_in_input + 1 

    # 4. Place the marker pixel into the output row at its original index
    output_row_array[marker_index] = 9 # Marker color is always 9
    
    # 5. Calculate the target start index for the colored block in the output row
    # Position is: right after marker + gap length
    new_block_start_index = marker_index + 1 + gap_length
    
    # 6. Place the colored block into the output row, handling boundaries
    if new_block_start_index < row_size: # Check if the start index is within the row bounds
        # Calculate the index where the block placement should end
        new_block_end_index_ideal = new_block_start_index + block_length 
        # Determine the actual end index, ensuring it doesn't exceed row size
        actual_new_end_index = min(new_block_end_index_ideal, row_size)
        # Place the block (or the part that fits)
        output_row_array[new_block_start_index : actual_new_end_index] = block_color

    # 7. Convert the numpy row back to a list and wrap it in another list for 1xN grid format
    output_grid = [output_row_array.tolist()]

    return output_grid