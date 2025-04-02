import numpy as np

"""
Identify a contiguous block of a color C (not white 0 or orange 7) and an orange marker (7) to its right. 
Fill the gap of white pixels (0) between the right edge of the block and the orange marker with color C.
"""

def find_main_block_and_marker(grid_row):
    """Finds the main colored block and the orange marker in a 1D grid row."""
    main_block_color = -1
    main_block_right_index = -1
    orange_marker_index = -1
    in_block = False

    for i, pixel in enumerate(grid_row):
        # Find the orange marker
        if pixel == 7:
            orange_marker_index = i
            # Stop searching for marker once found, but continue for block if needed

        # Find the main block
        if pixel != 0 and pixel != 7:
            if not in_block: # Start of a potential block
                 main_block_color = pixel
                 in_block = True
            elif pixel != main_block_color: # End of the block because color changed
                main_block_right_index = i - 1
                # If we found the marker already, we can stop early
                if orange_marker_index != -1:
                    break
                in_block = False # Reset for potential other blocks (though task implies one)
            # Continue in block of the same color
            main_block_right_index = i # Keep updating rightmost index while in block

        elif in_block and pixel == 0: # End of the block because we hit white
            # main_block_right_index is already set to the last non-zero index
             in_block = False
             # If we found the marker already, we can stop early
             if orange_marker_index != -1:
                 break

    # Handle case where block goes to the end of the row
    if in_block:
        main_block_right_index = len(grid_row) - 1
        
    # Handle case where marker is not found or block is not found (shouldn't happen based on examples)
    if main_block_color == -1 or orange_marker_index == -1:
        # Or maybe more robust error handling? Based on examples, this won't occur.
        print("Warning: Main block or orange marker not found as expected.")
        return None, -1, -1


    # Refine search: Ensure we pick the block immediately preceding the marker if multiple exist
    # For this specific task structure, the first block found *before* the marker is the correct one.
    # Let's re-scan specifically for the block ending right before the marker
    
    potential_block_color = -1
    potential_block_right_index = -1
    
    # Scan leftwards from the marker to find the end of the block
    for i in range(orange_marker_index - 1, -1, -1):
        pixel = grid_row[i]
        if pixel != 0 and pixel != 7: # Found the rightmost pixel of the block
            potential_block_right_index = i
            potential_block_color = pixel
            break # Found the block edge we care about
        elif pixel != 0 and pixel == 7: # Should not happen based on structure
             continue # Ignore other markers if any
        # else if pixel == 0, continue searching left

    if potential_block_color != -1:
         return potential_block_color, potential_block_right_index, orange_marker_index
    else:
         # Case where there's no block before the marker (e.g., marker at start or only white before it)
         print("Warning: No block found immediately before the orange marker.")
         return None, -1, -1


def transform(input_grid):
    """
    Transforms the input grid by filling the gap between a colored block and an orange marker.

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the grid row.

    Returns:
        np.array: The transformed 1D grid row as a numpy array.
    """
    # Ensure input is a numpy array for easier manipulation
    if not isinstance(input_grid, np.ndarray):
        grid = np.array(input_grid, dtype=int)
    else:
        grid = input_grid.copy() # Work on a copy

    # Assuming the grid is effectively 1D based on examples
    if grid.ndim > 1:
        if grid.shape[0] == 1:
            grid_row = grid[0]
        elif grid.shape[1] == 1:
             grid_row = grid[:, 0]
        else:
            # This case isn't represented in the examples.
            # Defaulting to the first row if ambiguous, but ideally handle based on task spec.
            print("Warning: Input grid is 2D, processing the first row.")
            grid_row = grid[0]
    else:
        grid_row = grid


    # Initialize output_grid as a copy of the relevant row
    output_row = grid_row.copy()

    # 1. Identify the main block color (C) and its rightmost index (R)
    # 2. Identify the orange marker (7) index (O)
    # Using a helper function for clarity
    block_color, block_right_index, marker_index = find_main_block_and_marker(grid_row)

    if block_color is None or block_right_index == -1 or marker_index == -1:
         # If elements not found as expected, return the original grid row
         print("Required elements not found, returning original row.")
         # Need to return in the original shape if it was 2D
         if grid.ndim > 1:
             if grid.shape[0] == 1:
                 return output_row.reshape(1, -1)
             elif grid.shape[1] == 1:
                 return output_row.reshape(-1, 1)
             else:
                  # Handle ambiguity - return original grid?
                  return input_grid.copy()
         else:
            return output_row


    # 3. Iterate from R + 1 up to (but not including) O
    # 4. Change pixels in this range to color C
    fill_start_index = block_right_index + 1
    fill_end_index = marker_index # Exclusive endpoint for range

    for i in range(fill_start_index, fill_end_index):
        # Only fill if the pixel is currently white (0), although examples imply it always is.
        # Based on observed transformation, we fill regardless of original color in gap.
        if i < len(output_row): # Basic bounds check
             output_row[i] = block_color

    # Return the modified row, potentially reshaping if original was 2D
    if grid.ndim > 1:
        if grid.shape[0] == 1:
            return output_row.reshape(1, -1)
        elif grid.shape[1] == 1:
            return output_row.reshape(-1, 1)
        else:
            # Ambiguous case: how to reconstruct the full 2D grid if only one row was processed?
            # Returning the modified first row embedded in original grid might be one interpretation.
            output_grid = input_grid.copy()
            output_grid[0] = output_row
            return output_grid
    else:
        return output_row
