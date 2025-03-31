import numpy as np

"""
Transformation Rule:
1. Create the output grid as a copy of the input grid.
2. Identify the row index ('separator_row_idx') containing only gray pixels (color 5). If not found, return the original grid.
3. Identify the row index ('sequence_row_idx') immediately above the separator line ('separator_row_idx' - 1). If invalid, return the original grid.
4. Extract the color sequence 'S' from the 'sequence_row', reading from left up to the column index ('last_seq_col') of the last non-white (0) pixel. Determine the length 'M' of sequence 'S'. If no sequence is found, return the original grid.
5. Locate the single 'trigger_pixel' below the 'separator_row_idx'. This pixel must not be white (0) or gray (5). Record its location '(r_trigger, c_trigger)'. If not found, return the original grid.
6. Iterate through each pixel '(r, c)' in the output grid:
    a. Calculate the Chebyshev distance: 'dist' = max(abs(r - r_trigger), abs(c - c_trigger)).
    b. If 'dist' is less than the sequence length 'M', set the color of the output grid pixel 'output_grid[r, c]' to 'S[dist]'.
7. Check if the trigger pixel's column index 'c_trigger' is identical to 'last_seq_col'.
8. If the column indices match, change the color of the pixel in the 'sequence_row' at column 'last_seq_col' (i.e., 'output_grid[sequence_row_idx, last_seq_col]') to gray (5).
9. Return the modified output grid.
"""

def find_separator_row(grid):
    """Finds the index of the row completely filled with gray (5)."""
    height, width = grid.shape
    for r_idx in range(height):
        row = grid[r_idx, :]
        # Check if row is not empty and all elements are 5
        if row.size > 0 and np.all(row == 5):
            return r_idx
    return -1 # Not found

def extract_sequence(grid, sequence_row_idx):
    """Extracts the color sequence and its properties from the specified row."""
    height, width = grid.shape
    if not (0 <= sequence_row_idx < height):
        return [], -1, -1 # Invalid row index

    row = grid[sequence_row_idx, :]
    last_non_white_col = -1
    # Find the last column index that is not white (0)
    for c_idx in range(width - 1, -1, -1):
        if row[c_idx] != 0:
            last_non_white_col = c_idx
            break
    
    if last_non_white_col == -1:
        return [], -1, -1 # Empty sequence or all white

    # Extract sequence up to the last non-white pixel
    sequence = list(row[:last_non_white_col + 1])
    sequence_len = len(sequence)
    return sequence, sequence_len, last_non_white_col

def find_trigger_pixel(grid, separator_row_idx):
    """Finds the trigger pixel below the separator line (non-white, non-gray)."""
    height, width = grid.shape
    if separator_row_idx < 0 or separator_row_idx >= height - 1: 
         # Separator not found or is the last row
         return None, -1
         
    for r in range(separator_row_idx + 1, height):
        for c in range(width):
            # Trigger pixel is not white (0) and not gray (5)
            if grid[r, c] != 0 and grid[r, c] != 5:
                # Found the first non-white, non-gray pixel below separator
                return (r, c), grid[r, c] 
    return None, -1 # Not found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Create the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 2. Identify the separator line.
    separator_row_idx = find_separator_row(output_grid)
    if separator_row_idx == -1:
        # Cannot proceed without separator
        # print("Separator row not found.")
        return output_grid 
        
    # 3. Identify the sequence row.
    sequence_row_idx = separator_row_idx - 1
    if sequence_row_idx < 0:
         # Cannot proceed if separator is the first row
         # print("Sequence row index invalid (separator is row 0?).")
         return output_grid

    # 4. Extract the color sequence S, its length M, and last column index.
    sequence, sequence_len, last_sequence_col_idx = extract_sequence(output_grid, sequence_row_idx)
    if not sequence:
        # Cannot proceed without a sequence
        # print("Sequence not found or empty.")
        return output_grid 
    # print(f"Sequence: {sequence}, Length: {sequence_len}, Last Col: {last_sequence_col_idx}")

    # 5. Locate the trigger pixel below the separator.
    trigger_loc, trigger_color = find_trigger_pixel(output_grid, separator_row_idx)
    if trigger_loc is None:
        # Cannot proceed without a trigger pixel
        # print("Trigger pixel not found.")
        return output_grid 
    r_trigger, c_trigger = trigger_loc
    # print(f"Trigger at: ({r_trigger}, {c_trigger}), Color: {trigger_color}")


    # 6. Draw the layered square structure using Chebyshev distance.
    for r in range(height):
        for c in range(width):
            # 6a. Calculate Chebyshev distance (max of absolute row/col differences).
            dist = max(abs(r - r_trigger), abs(c - c_trigger))
            
            # 6b. If within range, set color based on sequence index = dist.
            if dist < sequence_len:
                output_grid[r, c] = sequence[dist]

    # 7. Check if trigger column matches the last sequence element's column.
    # print(f"Comparing trigger column {c_trigger} with last sequence column {last_sequence_col_idx}")
    if c_trigger == last_sequence_col_idx:
        # 8. If they match, change the color in the sequence row at that column to gray (5).
        # Check bounds for safety
        if 0 <= sequence_row_idx < height and 0 <= last_sequence_col_idx < width:
             # print(f"Modifying sequence row {sequence_row_idx} at column {last_sequence_col_idx} to gray.")
             output_grid[sequence_row_idx, last_sequence_col_idx] = 5

    # 9. Return the modified output grid.
    return output_grid