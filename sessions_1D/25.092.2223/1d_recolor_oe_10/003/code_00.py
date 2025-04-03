import numpy as np # Although numpy isn't strictly needed for list processing, it's often used in ARC tasks. Keeping it for potential future use or consistency.

"""
Recolor contiguous segments of magenta (6) pixels in a 1D grid based on their length parity.
Segments with an odd number of pixels are changed to green (3).
Segments with an even number of pixels are changed to gray (5).
All other pixels (white, 0) remain unchanged. Assumes input is effectively a 1D list.
"""

def transform(input_grid):
    """
    Transforms a 1D input grid by recoloring magenta segments.

    Args:
        input_grid (list or list of lists): A grid represented as a list (for 1D)
                                             or list of lists (expecting a single inner list for 1D cases).

    Returns:
        list: The transformed 1D grid as a list.
    """

    # --- Input Processing ---
    # Standardize input to be a simple 1D list
    if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
         # If it's a list of lists (e.g., [[0, 6, 6,...]]), extract the first row.
         # This aligns with the ARC format where even 1D tasks might be nested.
         if len(input_grid) == 1:
             current_grid = input_grid[0]
         else:
            # This case shouldn't happen based on the examples, but as a fallback, process the first row.
            # A more robust solution might raise an error or handle multiple rows if the task spec changed.
            current_grid = input_grid[0]
            print("Warning: Input grid has multiple rows, processing only the first row.")
    elif isinstance(input_grid, list):
        # Input is already a 1D list
        current_grid = input_grid
    else:
        # Handle unexpected input types (e.g., numpy array directly) if necessary
        # For now, assume list or list of lists based on typical ARC task structure.
        raise TypeError("Input grid must be a list or a list of lists.")

    # Initialize output_grid as a copy of the processed input list
    output_grid = list(current_grid)
    n = len(current_grid)
    i = 0 # Current index for scanning the grid

    # --- Segment Identification and Recoloring ---
    # Iterate through the grid using the index 'i'
    while i < n:
        # Check if the current pixel is the target color (magenta, 6)
        if current_grid[i] == 6:
            # Found the start of a potential segment
            start_index = i
            segment_length = 0
            
            # Scan forward to find the end of the contiguous segment
            while i < n and current_grid[i] == 6:
                segment_length += 1
                i += 1 # Move index forward within the segment
            # 'i' now points to the first element *after* the segment or is == n

            # Determine the new color based on segment length parity
            # Odd length -> green (3)
            # Even length -> gray (5)
            new_color = 3 if segment_length % 2 != 0 else 5
            
            # Recolor the identified segment in the output grid
            # The loop goes from the start_index up to (but not including) the current index 'i'
            for j in range(start_index, i):
                output_grid[j] = new_color
            
            # Continue the outer loop: 'i' is already positioned correctly after the segment
        else:
            # Current pixel is not magenta, simply move to the next pixel
            i += 1
            
    # --- Return Result ---
    return output_grid