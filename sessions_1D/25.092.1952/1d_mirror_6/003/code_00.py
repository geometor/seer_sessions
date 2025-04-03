import numpy as np

def find_anchor_in_row(row_data, anchor_color=9):
    """
    Finds the column index of the first occurrence of the anchor pixel 
    in a given 1D array (row).
    Returns the column index or None if not found.
    """
    # Iterate through the row data with index
    for c_idx, pixel in enumerate(row_data):
        # Check if the pixel matches the anchor color
        if pixel == anchor_color:
            # Return the column index if found
            return c_idx
    # Return None if the loop completes without finding the anchor
    return None 

def find_payload_in_row(row_data, background_color=0, anchor_color=9):
    """
    Finds the first contiguous horizontal line of non-background, non-anchor 
    color in a given 1D array (row).
    Returns its color, starting column index, and length, or (None, None, None) 
    if not found.
    """
    width = len(row_data)
    # Iterate through the row data to find the start of the payload
    for c_idx in range(width):
        pixel = row_data[c_idx]
        # Check if the pixel is a potential payload color
        if pixel != background_color and pixel != anchor_color:
            # Check if this is the actual start of the line 
            # (i.e., it's the first pixel or the previous pixel is different)
            if c_idx == 0 or row_data[c_idx-1] != pixel:
                payload_color = pixel
                payload_col_start_in = c_idx
                payload_length = 0
                # Measure the length of the contiguous line of this color
                for k in range(c_idx, width):
                    if row_data[k] == payload_color:
                        payload_length += 1
                    else:
                        # Stop counting when the color changes or end of row
                        break 
                # Return the found payload details
                return payload_color, payload_col_start_in, payload_length
    # Return None if no payload line is found in the row
    return None, None, None 


def transform(input_grid):
    """
    Transforms an input grid based on finding an anchor pixel (maroon, 9) and a 
    horizontal payload line (any other non-white color) in the first row. 
    The payload line is moved to a new row (assumed to be row 1 in a 2-row 
    output grid) and its horizontal position is adjusted relative to the anchor.

    The transformation rule identified from examples is:
    The horizontal distance from the anchor's column to the END column of the 
    payload line in the input determines the horizontal distance from the 
    anchor's column to the START column of the payload line in the output.

    Assumptions derived from the provided examples:
    1. The anchor pixel (9) and the payload line exist and are located in the 
       first row/list element of the input_grid data structure.
    2. The required output grid always has a height of 2.
    3. The output grid has the same width as the input row where objects were found.
    4. The anchor's final position in the output grid is in row index 1, at the 
       same column index it occupied in the input row.
    5. The entire payload line moves to row index 1 in the output grid.
    """
    
    # --- Input Validation and Analysis ---
    # Check if input_grid is a list, is not empty, and its first element is also a list
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        print("Warning: Invalid input grid format. Expecting List[List[int]].")
        # Return an empty structure that matches the expected output format (2 rows)
        return [[], []] 
        
    # Attempt to convert the first row to a NumPy array for easier processing
    try:
        # Assume relevant objects are only in the first row/list element
        input_row_data = np.array(input_grid[0], dtype=int)
    except (ValueError, TypeError):
         print("Warning: Could not convert first input row to numpy array.")
         return [[], []] 

    input_width = len(input_row_data)
    # Handle case where the first row is empty
    if input_width == 0:
         print("Warning: Input row is empty.")
         return [[], []] # Return empty 2-row grid

    # --- Define Output Structure ---
    # Define expected output dimensions based on consistent example pattern
    output_height = 2 
    output_width = input_width
    # Define the assumed output row index for both anchor & payload based on examples
    r_output = 1 

    # --- Find Input Objects ---
    # Find the column index ('c_anchor') of the anchor pixel in the input row
    c_anchor = find_anchor_in_row(input_row_data, anchor_color=9)
    
    # Find payload details ('payload_color', 'c_payload_start_in', 'l_payload') in the input row
    payload_color, c_payload_start_in, l_payload = find_payload_in_row(input_row_data)

    # --- Handle Missing Objects ---
    # Check if either the anchor or the payload was not found
    if c_anchor is None or payload_color is None:
        # If essential components are missing, create a default output grid.
        print(f"Warning: Anchor {'found' if c_anchor is not None else 'NOT FOUND'}, Payload {'found' if payload_color is not None else 'NOT FOUND'}. Returning default grid.")
        # Create a 2xWidth grid filled with the background color (0).
        output_grid = np.zeros((output_height, output_width), dtype=int)
        # If the anchor *was* found, place it in its assumed output position.
        if c_anchor is not None:
            # Check bounds before placing anchor (should be safe given width calculation)
            if 0 <= r_output < output_height and 0 <= c_anchor < output_width:
                 output_grid[r_output, c_anchor] = 9 
        # Return the default grid (empty or with only anchor)
        return output_grid.tolist()

    # --- Transformation Calculation ---
    # Calculate the column index of the last pixel of the payload line in the input row
    c_payload_end_in = c_payload_start_in + l_payload - 1

    # Calculate the key horizontal distance: from anchor column to payload end column
    dist = c_anchor - c_payload_end_in
    
    # Calculate the starting column for the payload line in the output grid
    # The rule is: output_start_column = anchor_column + distance
    c_payload_start_out = c_anchor + dist
    
    # --- Populate Output Grid ---
    # Initialize the final output grid with the background color (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the anchor pixel in its assumed output position (row 'r_output', same column 'c_anchor')
    # Include basic bounds check for robustness, although should be valid by construction
    if 0 <= r_output < output_height and 0 <= c_anchor < output_width:
        output_grid[r_output, c_anchor] = 9
    
    # Draw the payload line at its new position in the output grid
    # The row is 'r_output', starting column is 'c_payload_start_out'
    for i in range(l_payload):
        current_col = c_payload_start_out + i
        # Check if the current column index is within the grid's width bounds
        if 0 <= current_col < output_width:
            # Place the payload pixel in the calculated position (row 'r_output')
            # This will overwrite the background '0'
            output_grid[r_output, current_col] = payload_color
            
    # Convert the final NumPy array grid back to a list of lists for the return value
    return output_grid.tolist()