import copy

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

def transform(input_grid):
    """
    Applies the color transformation based on green block length to a 1xN grid.

    Args:
        input_grid (list): A list containing a single list of integers 
                           representing the 1xN input grid.

    Returns:
        list: A list containing a single list of integers representing the 
              transformed 1xN output grid.
    """
    # Ensure input is in the expected format (list containing one list)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle error or unexpected format if necessary, here we assume correct format
        # For robustness, you might raise an error or return the input unchanged.
        # print("Warning: Input grid format might be incorrect.")
        # For now, attempt to process the first element if it's a list
        if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
           input_row = input_grid[0]
        else: # If input_grid itself is the row (list of ints) - adapt
             if isinstance(input_grid, list) and all(isinstance(x, int) for x in input_grid):
                 input_row = input_grid
             else:
                 # Cannot determine the row, return input or raise error
                 return copy.deepcopy(input_grid) # Return a copy to avoid side effects

    else: # Standard case
        input_row = input_grid[0]

    # Initialize the output row as a copy of the input row
    output_row = list(input_row)
    n = len(output_row)
    i = 0

    # Define the color mapping based on block length
    color_map = {
        1: 4,  # length 1 -> yellow
        2: 2,  # length 2 -> red
        3: 9   # length 3 -> maroon
    }

    # Iterate through the input row
    while i < n:
        # Check if the current pixel is green (3)
        if output_row[i] == 3: # Check the output_row as it's being modified
            # Found the start of a potential green block
            start_index = i
            current_length = 0
            # Measure the length of the contiguous green block
            # Use input_row for measurement to avoid issues if a block was already partially processed (shouldn't happen with this logic, but safer)
            while i < n and input_row[i] == 3: 
                current_length += 1
                i += 1 # Advance the main loop index as we measure

            # Determine the replacement color based on the measured length
            replacement_color = color_map.get(current_length)

            # If a valid replacement color exists (length was 1, 2, or 3)
            if replacement_color is not None:
                # Update the corresponding pixels in the output row
                for j in range(start_index, start_index + current_length):
                    # Check bounds just in case, though should be correct
                    if j < n: 
                        output_row[j] = replacement_color
            # If length wasn't in the map (e.g., length 0 or > 3), the original 
            # green pixels remain in output_row because we copied it initially.
            # The index 'i' is already advanced past the block by the inner while loop.
            
        else:
            # If the pixel is not green, just move to the next pixel
            i += 1

    # Wrap the processed row back into a list to match the 1xN grid format
    output_grid = [output_row]
    
    return output_grid
