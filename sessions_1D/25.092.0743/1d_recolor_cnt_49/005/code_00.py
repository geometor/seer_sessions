import copy
import numpy as np

"""
Transforms a 1xN input grid by identifying contiguous horizontal blocks of 
green (3) pixels within the single row and replacing them with a new color 
based on the length of the block.

- Blocks of length 1 are replaced with yellow (4).
- Blocks of length 2 are replaced with red (2).
- Blocks of length 3 are replaced with maroon (9).
- All other pixels, specifically white (0), remain unchanged.
The output grid retains the 1xN shape.
"""

# Define the mapping from green block length to output color
COLOR_MAP = {
    1: 4,  # yellow
    2: 2,  # red
    3: 9   # maroon
}
TARGET_COLOR = 3 # Green

def transform(input_grid):
    """
    Applies the color transformation based on green block length to a 1xN grid.

    Args:
        input_grid (list or np.array): A list containing a single list of integers 
                                      or a numpy array representing the 1xN 
                                      input grid.

    Returns:
        list: A list containing a single list of integers representing the 
              transformed 1xN output grid.
    """
    # Convert numpy array to list of lists if necessary
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        # Assuming input is already list of lists or similar structure
        input_list = input_grid

    # Validate input format and extract the row
    if not isinstance(input_list, list) or len(input_list) == 0 or not isinstance(input_list[0], list):
        # Attempt to handle if input_grid was passed as just the row list
        if isinstance(input_list, list) and all(isinstance(x, int) for x in input_list):
             input_row = input_list
        else:
             # If format is unexpected, return a deep copy or raise error
             print(f"Warning: Unexpected input format: {type(input_grid)}. Returning copy.")
             return copy.deepcopy(input_list) 
    else: # Standard case: input_list is [[...]]
        input_row = input_list[0]

    # Initialize the output row as a copy of the input row
    output_row = list(input_row) 
    n = len(input_row)
    i = 0 # Current position in the row

    # Iterate through the input row to find and process green blocks
    while i < n:
        # Check the original input row for the target color (green)
        if input_row[i] == TARGET_COLOR:
            # Found the start of a potential green block
            start_index = i
            current_length = 0
            
            # Measure the length of the contiguous green block in the input row
            while i < n and input_row[i] == TARGET_COLOR:
                current_length += 1
                i += 1 # Advance the main loop index as we measure
            
            # Determine the replacement color based on the measured length
            replacement_color = COLOR_MAP.get(current_length)

            # If a valid replacement color exists (length was 1, 2, or 3)
            if replacement_color is not None:
                # Update the corresponding pixels in the output row
                for j in range(start_index, start_index + current_length):
                    # Basic bounds check (shouldn't be necessary with correct logic)
                    if j < n: 
                        output_row[j] = replacement_color
            # If length wasn't in the map (e.g., length 0 or > 3), the original 
            # green pixels remain in output_row because we initialized it as a copy.
            # The index 'i' is already advanced past the block by the inner while loop.
            
        else:
            # If the pixel is not the target color, just move to the next pixel
            i += 1

    # Wrap the processed row back into a list of lists to match the required 1xN grid format
    output_grid = [output_row]
    
    return output_grid