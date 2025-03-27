import numpy as np

"""
Processes each row of the input grid independently. 
For the current row:
    a. Identify the column indices of all green (3) pixels.
    b. Create an empty set `occupied_destinations_this_row` to track columns filled by moved green pixels during this row's processing.
    c. Process the green pixels found in step 3a in order from rightmost column index to leftmost column index (`c`).
    d. For each green pixel at original column `c`:
        i. Determine its target column `target_c`: Scan leftwards from `c-1` down to 0 in the *original* row data. If an azure (8) pixel is found at column `az_c`, set `target_c = az_c + 1`. If no azure pixel is found, set `target_c = 0`.
        ii. If the green pixel's current column `c` is equal to `target_c`, do nothing and proceed to the next green pixel.
        iii. If `c` is not equal to `target_c`, calculate the final destination column `dest_c`:
            1. Initialize `dest_c = target_c`.
            2. While the column index `dest_c` is present in the `occupied_destinations_this_row` set: increment `dest_c` by 1.
            3. If `dest_c` is within the grid bounds (less than the grid width):
                A. Add the column index `dest_c` to the `occupied_destinations_this_row` set.
                B. Update the output grid: set the pixel at (current row, `c`) to white (0).
                C. Update the output grid: set the pixel at (current row, `dest_c`) to green (3).
Return the final output grid.
"""

def find_target_column(row_array, start_col):
    """
    Determines the target column for a green pixel based on azure pixels to its left.

    Args:
        row_array (np.array): The 1D numpy array representing the original row.
        start_col (int): The column index of the green pixel.

    Returns:
        int: The target column index.
    """
    target_c = 0  # Default target is column 0
    # Scan leftwards from start_col - 1 down to 0
    for c in range(start_col - 1, -1, -1):
        if row_array[c] == 8:  # Found an azure pixel
            target_c = c + 1  # Target is the column immediately to its right
            break  # Stop searching once the leftmost azure is found
    return target_c

def transform(input_grid):
    """
    Transforms the input grid by moving green pixels leftward based on azure pixel
    positions within each row, handling collisions by shifting right.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # Iterate through each row independently
    for r in range(height):
        # Get the original state of the current row for reference
        original_row = input_np[r, :]
        
        # Find column indices of all green pixels in the original row
        green_cols = np.where(original_row == 3)[0]
        
        # Keep track of destination columns occupied by *moved* green pixels in this row's pass
        occupied_destinations_this_row = set()

        # Process green pixels from right to left within the row
        for c in sorted(green_cols, reverse=True):
            
            # Determine the target column based on the original row state
            target_c = find_target_column(original_row, c)

            # Check if the pixel needs to move (current column is not the target column)
            if c == target_c:
                # If the pixel is already at its target, it doesn't move.
                # We don't mark this position as occupied yet, as only *moved* pixels cause stacking.
                # If another pixel later targets this stationary pixel's location, 
                # the collision resolution below will handle it by checking occupied_destinations_this_row.
                continue 

            # Calculate the final destination column, resolving collisions
            dest_c = target_c
            # While the candidate destination `dest_c` is already marked as occupied 
            # by a previously *moved* green pixel in this row's pass:
            while dest_c in occupied_destinations_this_row:
                 dest_c += 1
            
            # Check if the final destination is within the grid bounds
            if dest_c < width:
                # Mark the final destination column as occupied for this row's pass
                occupied_destinations_this_row.add(dest_c)

                # Update the output grid: 
                # Set original position to white (only if it's different from dest_c, which it is if we are here)
                output_grid[r, c] = 0  
                # Set final destination to green
                output_grid[r, dest_c] = 3 
            # else:
                # If dest_c >= width, the pixel cannot be placed according to the rules.
                # Based on analysis, this case might not occur in the provided examples.
                # If it did, the pixel effectively disappears or stays put depending on interpretation.
                # Current implementation: if it goes out of bounds, the original green pixel 
                # at (r, c) is simply erased (set to 0) and not placed anywhere else.
                # To make it stay put instead if it runs out of space:
                # else: output_grid[r, c] = 3 # Keep it in original place
                # Let's stick with erasing the original and not placing if out of bounds,
                # matching the idea of trying to move it.
                # Reconsider: The most logical thing if it can't move right is it just doesn't move at all.
                # Let's refine the logic: Only erase the original if the move is successful (within bounds).
                
                # --- Revised logic block for clarity ---
                # Start move attempt:
                # Find target_c (done above)
                # If c == target_c, continue (done above)
                
                # Calculate actual dest_c considering collisions
                # dest_c = target_c (initial)
                # while dest_c in occupied_destinations_this_row: dest_c += 1

                # Check if move is possible and perform it
                # if dest_c < width:
                #    occupied_destinations_this_row.add(dest_c)
                #    output_grid[r, c] = 0 # Erase original *only if move successful*
                #    output_grid[r, dest_c] = 3 # Place at destination
                # else:
                     # Pixel cannot be placed, it stays in its original position 'c'.
                     # No change needed to output_grid[r, c] as it started green.
                     # Do NOT add 'c' to occupied_destinations_this_row unless it was the target.
                     # Let's revise the entire block slightly for this specific handling:

            else: # dest_c >= width
                 # The pixel could not find a valid spot within the grid width due to collisions.
                 # In this scenario, the pixel remains in its original position.
                 # We do not change output_grid[r, c] (it's still green).
                 # We do not add anything to occupied_destinations_this_row.
                 # No action needed here, just proceed to the next green pixel.
                 pass


    # Convert the final numpy array back to list of lists for the expected output format
    return output_grid.tolist()