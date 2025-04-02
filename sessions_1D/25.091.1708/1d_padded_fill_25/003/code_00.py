import numpy as np
import copy

"""
Identifies pairs of identical non-white pixels (C) located in the same row of the input grid, 
where these pairs are separated horizontally only by white pixels (0). 
For each such identified pair (at columns col_start and col_end in a given row), 
it fills the horizontal segment from col_start to col_end (inclusive) in that row of the output grid with the color C. 
Pixels not part of such a filled segment remain unchanged from the input.
"""

def transform(input_grid):
    """
    Transforms the input grid by finding horizontal pairs of identical non-white pixels
    separated by only white pixels and filling the segment between them.

    Args:
        input_grid (list or np.array): A 2D list or NumPy array representing the input grid.

    Returns:
        np.array: A 2D NumPy array representing the transformed grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Iterate through each row
    for r in range(rows):
        # Use a while loop for the starting column index to allow skipping after a fill
        c_start = 0
        while c_start < cols:
            # Get the color of the potential starting pixel
            color_c = input_np[r, c_start]

            # Check if the current pixel is non-white (potential start of a pattern)
            if color_c != 0:
                found_pair = False
                # Search for the next pixel in the same row with the same color C
                for c_end in range(c_start + 1, cols):
                    if input_np[r, c_end] == color_c:
                        # Found a potential pair (color_c at c_start and c_end)
                        # Check if all pixels strictly between c_start and c_end are white (0)
                        is_gap_white = True
                        if c_end > c_start + 1: # Only check if there's actually a gap
                            # Slice the row between the two points (exclusive of endpoints)
                            gap_segment = input_np[r, c_start + 1 : c_end]
                            # Check if all elements in the gap segment are 0
                            if not np.all(gap_segment == 0):
                                is_gap_white = False
                        
                        # If the gap is white (or there's no gap), we found a valid pattern
                        if is_gap_white:
                            # Fill the segment (including the endpoints) in the output grid
                            output_grid[r, c_start : c_end + 1] = color_c
                            
                            # Set the outer loop index to continue searching *after* this filled segment
                            c_start = c_end 
                            found_pair = True
                            # Break the inner loop (c_end) since we found the first valid pair for this c_start
                            break 
                
                # Increment the starting column index for the next iteration
                # If a pair was found, c_start was updated to c_end, so this moves to c_end + 1
                # If no pair was found, this moves to the next column after the initial c_start
                c_start += 1

            else:
                # If the current pixel is white, just move to the next column
                c_start += 1

    # Return the modified grid as a NumPy array (common in ARC)
    # If the required output format is list of lists, convert back: return output_grid.tolist()
    return output_grid.tolist() # Convert back to list of lists as per ARC standard