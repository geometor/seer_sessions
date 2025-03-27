import numpy as np

"""
Processes each row of the input grid independently. 
For each row, identifies all green (3) pixels.
For each green pixel, determines its target destination column by finding the first azure (8) pixel to its left. 
The target is the column immediately to the right of this azure pixel. If no azure pixel is found to the left, the target is column 0.
Processes green pixels within a row from right to left. 
If a green pixel needs to move (its current column is not its target column), it is moved to the target column. 
If the target column is already occupied by another green pixel moved in the same row during this process, the current green pixel is placed in the next available column to the right.
The original position of a moved green pixel is set to white (0).
Pixels other than green and the vacated positions remain unchanged.
"""

def find_first_azure_left(row_array, start_col):
    """
    Scans leftwards in a row array from start_col-1 to find the first azure (8) pixel.
    
    Args:
        row_array (np.array): The 1D numpy array representing the row.
        start_col (int): The starting column index (exclusive) for the leftward scan.

    Returns:
        int: The column index of the first azure pixel found, or -1 if none is found.
    """
    for c in range(start_col - 1, -1, -1):
        if row_array[c] == 8:
            return c
    return -1

def transform(input_grid):
    """
    Transforms the input grid based on the rules described above.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # Iterate through each row
    for r in range(height):
        row_data = output_grid[r, :]
        
        # Find column indices of all green pixels in the current row
        green_cols = [c for c in range(width) if row_data[c] == 3]
        
        # Keep track of destination cells occupied in this row's processing pass
        occupied_destinations = set()

        # Process green pixels from right to left within the row
        for c in sorted(green_cols, reverse=True):
            
            # Find the first azure pixel to the left
            az_c = find_first_azure_left(row_data, c)

            # Determine the target column
            if az_c != -1:
                target_c = az_c + 1
            else:
                target_c = 0

            # Check if the pixel needs to move
            if c == target_c:
                 # If the pixel is already at its target, but another pixel might have moved *into* this spot
                 # we still need to mark it as occupied to prevent overwrites later in the right-to-left scan.
                 # However, based on the examples, it seems if a pixel starts at the correct spot, it stays,
                 # and collisions are resolved for pixels that *move* into occupied spots.
                 # Let's refine: If c == target_c, it stays, but we *should* track it if other moving pixels might target it.
                 # Simplification: If c == target_c, *don't move it*. If another pixel *targets* this c later, 
                 # collision resolution will handle it. Mark it occupied *only* if it *moves*.
                 # Let's stick to the original plan: only mark occupied if it *moves* to a new spot.
                 # If c == target_c, just continue.
                continue 

            # Resolve collisions: find the actual destination column
            dest_c = target_c
            # Check against existing pixels *and* newly occupied spots
            while dest_c < width and (output_grid[r, dest_c] != 0 or (r, dest_c) in occupied_destinations):
                 # Important edge case: If the target is blocked by a non-background color that isn't a newly moved green, 
                 # the logic needs clarification. The examples suggest stacking only occurs relative to other *moved* greens.
                 # Re-evaluating collisions: The rule seems to be stacking *relative to already moved greens* in the same pass.
                 # Let's check only against `occupied_destinations`.
                 # Correction: The while loop should check `occupied_destinations`, not `output_grid`.
                 # The examples show stacking pushes right.
                 
                 # Refined Collision Check:
                 # While the candidate destination `dest_c` is already marked as occupied *by a previously moved green pixel* in this row's pass
                while (r, dest_c) in occupied_destinations:
                     dest_c += 1
                 # Boundary check: Ensure dest_c doesn't go out of bounds
                 if dest_c >= width:
                      # This scenario (running out of space) isn't explicitly covered by examples, 
                      # but seems unlikely given grid size constraints and movement rules.
                      # For now, assume it fits or handle error/edge case later if needed.
                      # Let's assume it won't happen based on task constraints/design.
                      # If it did, the pixel might just stay? Or error? Let's proceed assuming it fits.
                      # If dest_c >= width, what happens? Let's print a warning for now if this occurs.
                       print(f"Warning: Pixel from ({r},{c}) could not be placed, destination {dest_c} out of bounds ({width}). Pixel not moved.")
                       continue # Skip moving this pixel if it goes out of bounds


            # Mark the final destination as occupied for this row's pass
            occupied_destinations.add((r, dest_c))

            # Update the output grid: clear original position, place green at destination
            output_grid[r, c] = 0  # Set original position to white
            output_grid[r, dest_c] = 3 # Set destination to green
            
            # Update row_data for subsequent `find_first_azure_left` calls *within the same row iteration*?
            # No, the azure positions are static obstacles. The `find_first_azure_left` should operate on the original state
            # or at least the state *before* any green pixels in the current row moved.
            # Let's use input_np[r, :] for finding azure positions to ensure consistency.
            # Re-run find_first_azure_left with input_np data:
            az_c = find_first_azure_left(input_np[r, :], c) # Use original row state for obstacle finding
            if az_c != -1:
                target_c = az_c + 1
            else:
                target_c = 0
            
            if c == target_c: # Re-check if movement is needed based on original state
                continue 
                
            dest_c = target_c
            while (r, dest_c) in occupied_destinations:
                 dest_c += 1
            if dest_c >= width:
                 print(f"Warning: Pixel from ({r},{c}) could not be placed, destination {dest_c} out of bounds ({width}). Pixel not moved.")
                 continue

            occupied_destinations.add((r, dest_c))
            output_grid[r, c] = 0 
            output_grid[r, dest_c] = 3


    # Convert back to list of lists for the expected output format
    return output_grid.tolist()