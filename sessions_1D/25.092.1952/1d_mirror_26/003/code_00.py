import numpy as np

"""
Transforms a 1xN input grid based on the following rules:
1.  Extract the single row of pixels from the input grid.
2.  Identify the single maroon pixel (9) marker and its index.
3.  Identify the contiguous sequence of non-white (0), non-maroon (9) pixels (the colored line), recording its color, length, start index, and end index.
4.  Calculate the gap length: the number of white pixels (0) strictly between the end of the colored line and the marker index.
5.  Calculate the new starting index for the colored line: the index immediately after the marker plus the calculated gap length.
6.  Create the output row by copying the input row.
7.  In the output row, erase the original colored line by setting its pixels to white (0).
8.  In the output row, draw the colored line (same color and length) starting at the calculated new position, ensuring it stays within the row bounds.
9.  Return the modified row packaged within a list to match the original 1xN grid format.
"""

def find_marker_1d(row):
    """
    Finds the index of the first occurrence of the marker color (maroon, 9) in a 1D array.

    Args:
        row (np.array): The 1D input row.

    Returns:
        int: The index of the marker, or None if not found.
    """
    marker_indices = np.where(row == 9)[0]
    if len(marker_indices) > 0:
        return marker_indices[0]
    else:
        return None # Marker not found

def find_colored_line_1d(row):
    """
    Finds the first contiguous block of non-white (0) and non-maroon (9) pixels in a 1D array.

    Args:
        row (np.array): The 1D input row.

    Returns:
        tuple: (line_color, line_length, line_start_index, line_end_index)
               or None if no such line is found.
    """
    line_color = -1
    line_length = 0
    line_start_index = -1
    line_end_index = -1
    in_line = False

    for i, pixel in enumerate(row):
        # A pixel is part of the line if it's not white (0) and not maroon (9)
        is_line_pixel = pixel != 0 and pixel != 9
        
        if is_line_pixel and not in_line:
            # Start of a potential line
            in_line = True
            line_color = pixel
            line_start_index = i
            line_length = 1
        elif is_line_pixel and in_line:
            # Continuing the line
            if pixel == line_color: # Ensure it's the same color
                line_length += 1
            else: 
                # Found a different color - this indicates the end of the first line
                line_end_index = i - 1
                # We only care about the first contiguous line based on examples
                break 
        elif not is_line_pixel and in_line:
            # End of the line (transitioned to white or maroon)
            line_end_index = i - 1
            in_line = False
            # Found the line, stop searching
            break
            
    # Handle case where the line goes to the very end of the grid
    if in_line:
        line_end_index = len(row) - 1

    if line_start_index != -1:
        return line_color, line_length, line_start_index, line_end_index
    else:
        return None # Line not found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Validate input and extract the single row
    # ARC tasks typically provide grids as lists of lists.
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
        # Handle unexpected format if necessary, though ARC format is consistent
        print("Warning: Unexpected input format. Assuming list of lists.")
        # Attempt to proceed if possible, otherwise return original
        if isinstance(input_grid, np.ndarray): # If it's already a numpy array
             if input_grid.ndim == 1: # If it's somehow 1D
                 row_np = input_grid
             elif input_grid.shape[0] == 1: # If it's Nx1 instead of 1xN
                 row_np = input_grid.flatten()
             else: # Cannot easily interpret
                 return input_grid # Return original
        else:
            return input_grid # Return original

    # Standard case: list of lists, extract first row
    row_np = np.array(input_grid[0], dtype=int)
    
    # Initialize output row as a copy of the input row
    output_row = row_np.copy()
    grid_len = len(row_np)

    # 2. Identify the marker
    marker_index = find_marker_1d(row_np)
    if marker_index is None:
        # print("Error: Marker (9) not found.")
        return input_grid # Return original if marker is missing

    # 3. Identify the colored line
    line_info = find_colored_line_1d(row_np)
    if line_info is None:
        # print("Error: Colored line not found.")
        return input_grid # Return original if line is missing
    line_color, line_length, line_start_index, line_end_index = line_info

    # 4. Calculate the gap length before the marker
    # Gap is the number of white pixels (0) between line_end_index and marker_index
    # If the line is right before the marker (e.g., ...5,9...), end_index+1 == marker_index, gap is 0.
    gap_before_length = marker_index - (line_end_index + 1)
    # Ensure gap is not negative (e.g. if line is AFTER marker initially, which shouldn't happen)
    gap_before_length = max(0, gap_before_length) 

    # 5. Calculate the new starting index for the colored line
    # The position starts immediately after the marker index.
    first_index_after_marker = marker_index + 1
    new_line_start_index = first_index_after_marker + gap_before_length

    # 6. Output row is already a copy

    # 7. Erase the original colored line by filling with white (0)
    # Ensure indices are valid before slicing
    if 0 <= line_start_index <= line_end_index < grid_len:
         output_row[line_start_index : line_end_index + 1] = 0
    else:
        # print("Warning: Invalid indices for original line.")
        # This indicates an issue with find_colored_line_1d or unexpected input
        return input_grid # Return original

    # 8. Place the colored line at the new position
    new_line_end_index = new_line_start_index + line_length
    
    # Ensure the placement does not exceed grid bounds
    # Calculate the actual portion of the line that fits
    actual_start_index = max(0, new_line_start_index) # Don't start before index 0
    actual_end_index = min(new_line_end_index, grid_len) # Don't go past the end
    
    # Determine how much of the line segment to actually draw based on bounds
    segment_length_to_draw = actual_end_index - actual_start_index
    
    if segment_length_to_draw > 0:
        # Place the line segment (color repeated) into the calculated slice
        output_row[actual_start_index : actual_end_index] = line_color
    
    # If segment_length_to_draw < line_length, the line was truncated. This doesn't happen in examples.

    # 9. Return the modified row in the original 1xN grid format (list of lists)
    return [output_row.tolist()]
