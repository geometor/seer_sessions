import copy

"""
Identifies the single contiguous horizontal segment of non-white pixels 
in the input row (assuming a single-row grid). It keeps the 
first (leftmost) and last (rightmost) pixel of this segment and changes 
all pixels strictly between them to white (0). Pixels outside the segment, 
and segments of length 1 or 2, remain unchanged. If no non-white segment is found,
the input is returned unchanged.
"""

def find_horizontal_segment(row):
    """
    Finds the start and end indices of the first contiguous horizontal 
    segment of non-white pixels in a single row.

    Args:
        row (list[int]): A single row list of pixel values.

    Returns:
        tuple[int, int]: A tuple containing the start and end index (inclusive). 
                         Returns (-1, -1) if no non-white pixel is found or the row is empty.
    """
    start_index = -1
    end_index = -1
    
    if not row: # Handle empty row
        return -1, -1
        
    in_segment = False
    for i, pixel in enumerate(row):
        # Look for the start of the segment
        if pixel != 0 and not in_segment:
            start_index = i
            end_index = i # Initialize end_index
            in_segment = True
        # Update the end if we are inside the segment and see a non-white pixel
        elif pixel != 0 and in_segment:
            end_index = i
        # Stop looking once we exit the first segment (hit a 0 after being in)
        # This implicitly assumes only the *first* segment matters if multiple exist
        elif pixel == 0 and in_segment:
            # The segment ended at the previous index (end_index is already correct)
            break 

    # If loop finished without finding a segment start_index remains -1
    # If loop finished while still in segment (segment reaches end), end_index is correct.
    
    return start_index, end_index

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.

    Args:
        input_grid (list[list[int]]): A grid represented as a list of lists,
                                      expected to have only one row.

    Returns:
        list[list[int]]: The transformed grid, also containing a single row,
                         or an empty list if the input format is invalid,
                         or the original grid if no modification is needed.
    """
    # --- Input Validation ---
    # Check if input is a list containing exactly one list (the row)
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
         # Return a copy of the input for unexpected formats, or consider raising error
         # For ARC compliance, often returning input or empty list is preferred over errors.
         # Let's return a deepcopy to avoid modifying the original input object if passed around.
         return copy.deepcopy(input_grid)
         
    # Check if it has exactly one row. If not, return input unmodified.
    if len(input_grid) != 1:
        return copy.deepcopy(input_grid)

    # Extract the single row
    input_row = input_grid[0]
    
    # Handle empty row case - return grid containing an empty row
    if not input_row:
        return [[]] 

    # --- Initialization ---
    # Create a copy of the input row to modify for the output
    # A shallow copy using list() is sufficient for a list of integers
    output_row = list(input_row) 

    # --- Locate Segment ---
    # Find the start and end indices of the first non-white segment
    start_index, end_index = find_horizontal_segment(input_row)

    # --- Apply Transformation ---
    # Check if a valid segment was found (start_index != -1)
    # And if the segment is long enough to be hollowed out (length > 2)
    # Segment length = end_index - start_index + 1
    # So, length > 2 means end_index - start_index + 1 > 2, or end_index - start_index > 1
    # Which simplifies to end_index > start_index + 1
    if start_index != -1 and end_index > start_index + 1:
        # Iterate through the indices strictly *between* the start and end indices
        # The range goes from start_index + 1 up to (but not including) end_index
        for i in range(start_index + 1, end_index):
            # Ensure index is valid before modification (should be, but defensive check)
            if 0 <= i < len(output_row):
                 # Set the pixel in the output row to white (0)
                 output_row[i] = 0
            # else: # Optional: handle unexpected index error
                 # print(f"Warning: Index {i} out of bounds for row length {len(output_row)}")
                 # pass 
    
    # --- Format Output ---
    # Return the modified row, wrapped in a list to match ARC grid format
    return [output_row]